from django.views import View
from django.http  import JsonResponse

from products.models import *

class CategoryView(View):
    def get(self,request,category_id):
        category = Category.objects.get(id=category_id)

        products_list = [{
            'name'  : product.name,
            'price' : product.price,
            'images': [image.image_url for image in product.picture_set.all()]
        } for product in category.product_set.all()]

        return JsonResponse({'product_list' : products_list} , status = 200)
        
class ProductView(View):
    def get(self,request,category_id,product_id):
        product = Category.objects.get(id = category_id).product_set.all()[product_id-1]

        product_information = {
            'name'       : product.name,
            'origin'     : product.origin,
            'volume'     : product.volume,
            'description': product.description,
            'summary'    : product.summary,
            'price'      : product.price,
            'stock'      : product.stock,
            'images'     : [image.image_url for image in product.picture_set.all()]  
        }

        return JsonResponse({'product_information' : product_information} , status = 200)