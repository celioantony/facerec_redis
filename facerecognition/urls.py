from django.urls import path
from . import views

urlpatterns = [
    # path('', views.cart),
    path('training', views.training, name='training'),
    path('recognition', views.recognition, name='recognition'),
    path('facerecognition', views.face_recognition_image),
]
