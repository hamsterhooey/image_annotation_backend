from django.urls import path
from .views import ImageListView, ImageDetailUpdateDeleteView, BoundingBoxListView, BoundingBoxDetailUpdateDeleteView

app_name = 'images'

urlpatterns = [
    path('', ImageListView.as_view()),
    path('bbs', BoundingBoxListView.as_view()),
    path('bbs/<sid>', BoundingBoxDetailUpdateDeleteView.as_view()),
    path('<sid>', ImageDetailUpdateDeleteView.as_view()),
]