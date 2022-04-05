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