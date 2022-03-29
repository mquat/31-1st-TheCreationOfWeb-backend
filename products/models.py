from django.db import models

class Category(models.Models):
    name       = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'

class Product(models.Model):
    category      = models.ForeignKey('Category', on_delete=models.CASCADE)
    name          = models.CharField(max_length=100)
    origin        = models.CharField(default='국산')
    weight_volume = models.IntegerField(max_length=100)
    description   = models.TextField()
    price         = models.IntegerField(max_length=100)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'

class Picture(models.Model):
    product    = models.ForeignKey('Product', on_delete=models.CASCADE)
    img        = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pictures'

