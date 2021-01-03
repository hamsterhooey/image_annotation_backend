from rest_framework import serializers
from .models import Image, BoundingBox


class BoundingBoxSerializer(serializers.ModelSerializer):
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

        try: # if the request contains information about boundingbox
            boundingboxes_data = validated_data.pop('boundingboxes')
            print(f"Boundingbox:{boundingboxes_data}")
        except:
            return instance

        keep_boundingboxes = [] # sids of bounding boxes that will be kept
        
        for boundingbox_data in boundingboxes_data: # Loop through each boundingbox json in request
            if 'sid' in boundingbox_data.keys(): # If the boundingbox json contains an sid, then update that boundingbox with new coordinates
                if BoundingBox.objects.filter(sid=boundingbox_data['sid']).exists(): # If a boundingbox with that sid already exists, then modify the coordinates, else do nothing
                    bb = BoundingBox.objects.get(sid=boundingbox_data['sid']) # Get the boundingbox with same sid
                    bb.coordinates = boundingbox_data.get('coordinates', bb.coordinates) # Update the coordinates with new data or if not present then with the previous data
                    bb.code = boundingbox_data.get('code', bb.code)
                    bb.save() 
                    keep_boundingboxes.append(bb.sid) # Append the sid to the list of boundingboxes to be kept
                else:
                    continue
            else: # If the boundingbox json doesn't contain sid then create a new boundingbox
                bb = BoundingBox.objects.create(**boundingbox_data, image=instance)  
                keep_boundingboxes.append(bb.sid)

        
        for boundingbox in instance.boundingboxes.all(): # Delete all of the other sid boundingboxes
            if boundingbox.sid not in keep_boundingboxes:
                boundingbox.delete()

        return instance