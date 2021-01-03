from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from images.models import Image, BoundingBox
from images.serializers import ImageSerializer, BoundingBoxSerializer

class ImageListView(ListAPIView):
    queryset = Image.objects.order_by('-created_at')
    serializer_class = ImageSerializer
    permission_classes = (permissions.AllowAny, )

class ImageDetailUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.order_by('-created_at')
    serializer_class = ImageSerializer
    lookup_field = 'sid'
    permission_classes = (permissions.AllowAny, )


class BoundingBoxListView(ListAPIView):
    queryset = BoundingBox.objects.order_by('-created_at')
    serializer_class = BoundingBoxSerializer
    permission_classes = (permissions.AllowAny, )


class BoundingBoxDetailUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = BoundingBox.objects.order_by('-created_at')
    serializer_class = BoundingBoxSerializer
    lookup_field = 'sid'
    permission_classes = (permissions.AllowAny, )
