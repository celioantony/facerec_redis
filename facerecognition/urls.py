from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('training', views.training, name='training'),
    path('recognition', views.recognition, name='recognition'),
    path('uploadtraining', views.face_upload_training),
    path('facerecognition', views.face_recognition_image),
]
