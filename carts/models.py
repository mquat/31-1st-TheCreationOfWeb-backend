from django.db import models

class Cart(models.Model):
    order          = models.ForeignKey('Purchase', on_delete=models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product        = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    cart_status    = models.ForeignKey('Cart_State', on_delete=models.CASCADE)
    count          = models.IntegerField()
    price          = models.DecimalField(max_digits=10, decimal_places=0)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

class Cart_State(models.Model):
    status_code = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_status'

class Purchase(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status     = models.ForeignKey('Purchase_State', on_delete=models.CASCADE)
    price      = models.DecimalField(max_digits=10, decimal_places=0)
    shipment   = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'purchases'

class Purchase_State(models.Model):
    status_code = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'purchase_status'