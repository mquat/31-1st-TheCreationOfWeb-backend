import json

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Sum

from users.utils     import login_decorator
from carts.models    import Cart
from products.models import Product

class CartListView(View):
    @login_decorator
    def get(self,request):
        carts = Cart.objects.filter(user = request.user).select_related('product').prefetch_related('product__picture_set')

        result = [{
            'id'       : cart.id,
            'images'   : [image.image_url for image in cart.product.picture_set.all()],
            'name'     : cart.product.name,
            'price'    : cart.product.price,
            'quantity' : cart.quantity
        } for cart in carts]

        total_price = Cart.objects.filter(user = request.user).aggregate(Sum('price'))

        return JsonResponse({'cart_list' : result, 'total_price' : total_price['price__sum']} , status = 200)

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        product_price = Product.objects.get(id = data['product_id']).price

        cart, is_created = Cart.objects.get_or_create(
            user        = request.user,  
            product_id  = data['product_id'], 
            defaults    = {
                'price'    : data['quantity'] * product_price,
                'quantity' : data['quantity']
            },
        )

        if not is_created:
            cart.quantity += data['quantity']
            cart.price    += data['quantity'] * product_price
            cart.save() 

        return JsonResponse({'message':'success'}, status=201)

    @login_decorator
    def patch(self,request,cart_id):
        data = json.loads(request.body)

        if data['quantity'] < 1:
            return JsonResponse({'message' : 'QUANTITY_UNDER_1_ERROR'} , status = 400)
        
        cart          = Cart.objects.get(id = cart_id)
        cart.quantity = data['quantity']
        cart.price    = data['quantity'] * cart.product.price
        cart.save()

        total_price = Cart.objects.filter(user = request.user).aggregate(Sum('price'))
        
        return JsonResponse({'total_price' : total_price['price__sum']} , status = 200)

    @login_decorator
    def delete(self, request):
        cart_ids = request.GET.getlist('cart_id')

        Cart.objects.filter(id__in = cart_ids, user = request.user).delete()
        
        return JsonResponse({'message':'NO_CONTENT'}, status=204)