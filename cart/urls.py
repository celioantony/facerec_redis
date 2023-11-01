from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_cart),
    path('addtocart', views.add_to_cart),
    path('increaseitem', views.increase_quantity),
    path('decreaseitem', views.decrease_quantity)
]
