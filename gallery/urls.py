from django.urls import path
from .views import gallery, gallery_upload

urlpatterns = [
    path('', gallery, name="gallery"),
    path('uploads/', gallery_upload, name="gallery_upload"),
]
