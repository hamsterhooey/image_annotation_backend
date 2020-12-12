from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from images.models import Image
from images.serializers import ImageSerializer

class ImageListView(ListAPIView):
    queryset = Image.objects.order_by('-date_created')
    serializer_class = ImageSerializer
    lookup_field = 'sid'
    permission_classes = (permissions.IsAuthenticated, )

class ImageDetailView(RetrieveAPIView):
    queryset = Image.objects.order_by('-date_created')
    serializer_class = ImageSerializer
    lookup_field = 'sid'
    permission_classes = (permissions.IsAuthenticated, )