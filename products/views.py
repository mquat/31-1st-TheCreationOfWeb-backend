import json

from django.views import View
from django.http  import JsonResponse

from .models import Category

class CategoryView(View):
    def get(self,request,category_id):
        category = Category.objects.get(id=category_id)

        result = [{
            'name'     : product.name,
            'price'    : product.price,
            'image_url': [image.image_url for image in product.picture_set.all()]
        } for product in category.product_set.all()]

        return JsonResponse({'product_list':result}, status=200)

class ProductView(View):
    def get(self,request,category_id,product_id):
        product = Category.objects.get(id=category_id).product_set.all()[product_id-1]
        result = {
            'name'        : product.name,
            'origin'      : product.origin,
            'volume'      : product.volume,
            'description' : product.description,
            'summary'     : product.summary,
            'price'       : product.price,
            'stock'       : product.stock,
            'image_url'   : [image.image_url for image in product.picture_set.all()]
            }  
                
        return JsonResponse({'product_info':result}, status=200)





