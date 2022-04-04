from django.views import View
from django.http  import JsonResponse

from products.models import *

class ProductListView(View):
    def get(self,request):
        category_id = int(request.GET.get('category_id' , None))
        offset      = request.GET.get('offset' , None)
        limit       = request.GET.get('limit' , None)

        if offset == None:
            offset = 0
        if limit == None:
            limit  = 10
        
        products = Product.objects.filter(category_id = category_id)[int(offset) : int(offset)+int(limit)]

        products_list = [{
            'id'     : product.id,
            'name'   : product.name,
            'price'  : product.price,
            'images' : [image.image_url for image in product.picture_set.all()]
        } for product in products]

        return JsonResponse({'product_list' : products_list} , status = 200)