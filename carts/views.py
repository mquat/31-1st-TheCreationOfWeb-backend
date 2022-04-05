import json

from django.urls import View
from django.http import JsonResponse

from carts.models import Cart

class CartView(View):
    def patch(self,request):
        # request 에는 id 와 quantity 들어간다
        user = request.user
        data = json.loads(request.body)
        product_id = data['id']
        quantity = data['quantity']

        Cart.objects.filter(user = request.body)
        #return 바뀐 quantity, 총 금액