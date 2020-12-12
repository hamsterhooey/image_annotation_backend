from django.urls import path
from .views import ImageListView, ImageDetailView

app_name = 'images'

urlpatterns = [
    path('', ImageListView.as_view()),
    path('<sid>', ImageDetailView.as_view()),
]