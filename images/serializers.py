from rest_framework import serializers
from .models import Image, BoundingBox


class BoundingBoxSerializer(serializers.ModelSerializer):
    # This part is super important otherwise validated_data doesn't get the sid
    sid = serializers.UUIDField(required=False)

    class Meta:
        model = BoundingBox
        fields = ('sid', 'created_at', 'image', 'code', 'coordinates')


class ImageSerializer(serializers.ModelSerializer):
    boundingboxes = BoundingBoxSerializer(many=True)
    class Meta:
        model = Image
        fields = ('sid', 'created_at', 'raw_file', 'boundingboxes', 'distance')
        lookup_field = 'sid'

    def create(self, validated_data):
        boundingboxes_data = validated_data.pop('boundingboxes')
        image = Image.objects.create(**validated_data)
        for boundingbox_data in boundingboxes_data:
            BoungingBox.objects.create(image=image, **boundingbox_data)
        return image

    def update(self, instance, validated_data):
        # First update the non-nested-serializer image fields
        instance.distance = validated_data.get('distance', instance.distance) # Instance refers to image
        instance.save()

        # If request contains "boundingboxes" then proceed with this logic. Else return instance with updated distance
        try:
            boundingboxes_data = validated_data.pop('boundingboxes')
        except:
            print("No bounding boxes in request")
        else:
            print(f"Boundingbox:{boundingboxes_data}")
            keep_boundingboxes = [] # sids of bounding boxes that will be kept
                
            for boundingbox_data in boundingboxes_data: # Loop through each boundingbox json in request
                if 'sid' in boundingbox_data.keys(): # If the boundingbox json contains an sid, then update that boundingbox with new coordinates
                    print("\nLogging\n")
                    if BoundingBox.objects.filter(sid=boundingbox_data['sid']).exists(): # If a boundingbox with that sid already exists, then modify the coordinates, else do nothing
                        bb = BoundingBox.objects.get(sid=boundingbox_data['sid']) # Get the boundingbox with same sid
                        bb.coordinates = boundingbox_data.get('coordinates', bb.coordinates) # Update the coordinates with new data or if not present then with the previous data
                        bb.code = boundingbox_data.get('code', bb.code)
                        bb.save() 
                        keep_boundingboxes.append(bb.sid) # Append the sid to the list of boundingboxes to be kept
                    else:
                        continue
                else: # If the boundingbox json doesn't contain sid then create a new boundingbox
                    print("Creating new bounding box")
                    bb = BoundingBox.objects.create(image=instance, **boundingbox_data,)  
                    keep_boundingboxes.append(bb.sid)
            
            # for boundingbox in instance.boundingboxes.all(): # Delete all of the other sid boundingboxes
            #     if boundingbox.sid not in keep_boundingboxes:
            #         print(f"Deleting BB with sid {boundingbox.sid}")
            #         boundingbox.delete()
        finally:
            return instance