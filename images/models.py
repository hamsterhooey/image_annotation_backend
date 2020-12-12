from django.db import models
import uuid

class Image(models.Model):
    sid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=100)
    s3_location = models.CharField(max_length=100)
    raw_image = models.ImageField() 

    def __str__(self):
        return self.filename