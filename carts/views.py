import json

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from users.utils  import login_decorator
from carts.models import Cart

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
    def delete(self, request):
        try: 
            data = json.loads(request.body) 

            user    = request.user
            product = data['id']

            if product == 0:
                Cart.objects.filter(user=user).delete()
                return JsonResponse({'message':'ALL_DELETED'}, status=204)
            
            Cart.objects.get(user=user, product=product).delete() 

            return JsonResponse({'message':'ITEM_DELETED'}, status=204)
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=401)