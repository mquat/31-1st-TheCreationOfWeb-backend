from django.db import models

class User(models.Model):
    user         = models.CharField(max_length=30, unique=True)
    password     = models.CharField(max_length=200)
    address      = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=30, unique=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    deleted_at   = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'

class Like(models.Model):
    user    = models.ForeignKey('User',on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'likes'