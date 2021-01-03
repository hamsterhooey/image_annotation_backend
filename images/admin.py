from django.contrib import admin

from .models import Image, BoundingBox

admin.site.register(Image)
admin.site.register(BoundingBox)