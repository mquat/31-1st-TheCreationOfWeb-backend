from django.views import View
from django.http  import JsonResponse

from products.models import *

class ProductListView(View):
    def get(self,request):
        category_id = request.GET.get('category_id' , None)
        products    = Product.objects.filter(category_id = category_id)

        products_list = [{
            'name'  : product.name,
            'price' : product.price,
            'images': [image.image_url for image in product.picture_set.all()]
        } for product in products]

        return JsonResponse({'product_list' : products_list} , status = 200)