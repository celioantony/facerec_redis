from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Cart(models.Model):
    OPEN='OP'
    IN_PROGRESS='IP'
    CLOSE='CL'
    CART_STATUS_CHOICES=[
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In Progress'),
        (CLOSE, 'Close')
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, through='AddedProducts')
    status = models.CharField(max_length=2, choices=CART_STATUS_CHOICES, default=OPEN)


class AddedProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    total = models.FloatField()
