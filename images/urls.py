from django.urls import path
from .views import ImageListView, ImageDetailUpdateView, BoundingBoxListView, BoundingBoxDetailUpdateView

app_name = 'images'

urlpatterns = [
    path('', ImageListView.as_view()),
    path('bbs', BoundingBoxListView.as_view()),
    path('bbs/<sid>', BoundingBoxDetailUpdateView.as_view()),
    path('<sid>', ImageDetailUpdateView.as_view()),
]