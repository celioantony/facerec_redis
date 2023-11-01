from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=255)
