from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart),
    path('recognition', views.recognition, name='recognition'),
    path('facerecognition', views.face_recognition_image),
    path('create', views.create_cart),
    path('addtocart', views.add_to_cart),
    path('increaseitem', views.increase_quantity),
    path('decreaseitem', views.decrease_quantity)
]
