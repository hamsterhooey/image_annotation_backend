from django.contrib.postgres.fields import ArrayField
from django.db import models
from PIL import Image
import uuid, pathlib

def image_upload_path(instance, filename):
    """Change the uploaded image's filename"""
    ext = pathlib.Path(filename).suffix
    return f'{instance.sid}{ext}'

class BaseModel(models.Model):
    sid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class Image(BaseModel):
    raw_file = models.ImageField(upload_to=image_upload_path) 
    distance = models.TextField(max_length=10, default='Not Set')

    def __str__(self):
        return self.raw_file.name

class BoundingBox(BaseModel):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='boundingboxes')
    code = models.CharField(max_length=20, default='Not Set')
    coordinates = ArrayField(models.IntegerField(), size = 4)

    def __str__(self):
        return self.code