import json

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from users.utils     import login_decorator
from products.models import Product
from carts.models    import Cart

class CartListView(View):
    @login_decorator
    def get(self,request):
        try:       
            carts = Cart.objects.filter(user = request.user).select_related('product').prefetch_related('product__picture_set')

            result = [{
                'id'       : cart.product.id,
                'images'   : [image.image_url for image in cart.product.picture_set.all()],
                'name'     : cart.product.name,
                'price'    : cart.product.price,
                'quantity' : cart.quantity
            } for cart in carts]

            total_price = 0

            for cart in carts:
                total_price += cart.price

            return JsonResponse({'cart_list' : result, 'total_price' : total_price} , status = 200)

        except ValidationError as e:
            return JsonResponse({'message' : e.message} , status = 401)

    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            cart, is_created = Cart.objects.get_or_create(
                user        = request.user,  
                product_id  = data['product_id'], 
                defaults     = {
                'price'    : data['price'],
                'quantity' : data['quantity']
                },
            )

            if not is_created:
                cart.quantity += data['quantity']
                cart.save() 

            # carts = [{
            #     'image_url' : [image.image_url for image in item.product.picture_set.all()],
            #     'name'      : item.product.name,
            #     'price'     : item.price,
            #     'quantity'  : item.quantity 
            # } for item in Cart.objects.filter(user = request.user)]

            return JsonResponse({'message':'success'}, status=201)
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=401)

    @login_decorator
    def delete(self, request):
        try: 
            # data = json.loads(request.body)
            cart_id = request.GET.getlist('cart_id')
            Cart.objects.filter(id__in = cart_id, user = request.user).delete()
            return JsonResponse({'message':'NO_CONTENT'}, status=204)
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=401)