import json

from django.forms import ValidationError
from django.http  import JsonResponse
from django.views import View

from users.utils     import login_decorator
from products.models import Product
from .models         import Cart

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

            summary = [{
                'image_url' : [image.image_url for image in item.product.picture_set.all()],
                'name'      : item.product.name,
                'price'     : item.price,
                'quantity'  : item.quantity 
            } for item in Cart.objects.filter(user=user)]

            return JsonResponse({'message':summary}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=401)