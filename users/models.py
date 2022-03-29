from django.db import models

class User(models.Model):
    user         = models.CharField(max_length=30, unique=True)
    password     = models.CharField(max_length=100)
    address      = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30, unique=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
