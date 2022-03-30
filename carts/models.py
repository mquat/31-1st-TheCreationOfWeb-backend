from django.db import models

class Cart(models.Model):
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product        = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity       = models.IntegerField()
    price          = models.DecimalField(max_digits=10,decimal_places=2)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

class Order_Item(models.Model):
    order          = models.ForeignKey('Order', on_delete=models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product        = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity       = models.IntegerField()
    price          = models.DecimalField(max_digits=10,decimal_places=2)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_items'

class Order(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status      = models.ForeignKey('Order_State', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipment    = models.IntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'

class Order_State(models.Model):
    status_code = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders_status'