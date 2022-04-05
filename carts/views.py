import json

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from users.utils     import login_decorator
from carts.models    import Cart
from products.models import Product

class CartView(View):
    @login_decorator
    def get(self,request):
        try:       
            carts = Cart.objects.filter(user = request.user).select_related('product')

            cart_list = [{
                'id'       : cart.product.id,
                'images'   : [image.image_url for image in cart.product.picture_set.all()],
                'name'     : cart.product.name,
                'price'    : cart.product.price,
                'quantity' : cart.quantity
            } for cart in carts]

            return JsonResponse({'cart_list' : cart_list} , status = 200)
        except ValidationError as e:
            return JsonResponse({'message' : e.message} , status = 401)

    @login_decorator
    def patch(self,request):
        try:
            data    = json.loads(request.body)
            product = Product.objects.get(id = data['id'])

            if data['quantity'] < 1:
                return JsonResponse({'message' : 'QUANTITY_UNDER_1_ERROR'} , status = 400)
            
            cart_modification = Cart.objects.filter(user = request.user , product = product)
            cart_modification.update(quantity = data['quantity'] , price = data['quantity'] * product.price)

            total_price = 0
            for cart in Cart.objects.filter(user = request.user):
                total_price += cart.price
            
            return JsonResponse({'total_price' : total_price} , status = 200)
        except ValidationError as e:
            return JsonResponse({'message' : e.message} , status = 401)