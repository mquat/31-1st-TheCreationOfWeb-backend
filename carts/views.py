import json

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from users.utils     import login_decorator
from products.models import Product
from carts.models    import Cart

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

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            user             = request.user
            product          = Product.objects.get(id=data['product_id'])
            cart_product     = Cart.objects.filter(user=user, product=product)
            current_quantity = 0 

            if cart_product.exists():
                current_quantity = Cart.objects.get(user=user, product=product).quantity 

            cart, created = Cart.objects.update_or_create(
                user     = user,  
                product  = product, 
                price    = data['price'],
                defaults = {'quantity':data['quantity']+current_quantity},
            )

            carts = [{
                'image_url' : [image.image_url for image in item.product.picture_set.all()],
                'name'      : item.product.name,
                'price'     : item.price,
                'quantity'  : item.quantity 
            } for item in Cart.objects.filter(user=user)]

            return JsonResponse({'message':carts}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=401)