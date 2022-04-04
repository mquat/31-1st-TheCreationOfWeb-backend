from django.views import View
from django.http  import JsonResponse

from products.models import *

class ProductListView(View):
    def get(self,request):
        category_id = int(request.GET.get('category_id' , None))
        offset      = request.GET.get('offset' , 0)
        limit       = request.GET.get('limit' , 10)
        
        products = Product.objects.filter(category_id = category_id)[int(offset) : int(offset)+int(limit)]

        products_list = [{
            'id'     : product.id,
            'name'   : product.name,
            'price'  : product.price,
            'images' : [image.image_url for image in product.picture_set.all()]
        } for product in products]

        return JsonResponse({'product_list' : products_list} , status = 200)

class ProductDetailView(View):
    def get(self,request,product_id):
        try:
            product = Product.objects.get(id = product_id)

            product_detail = {
                'name'        : product.name,
                'origin'      : product.origin,
                'volume'      : product.volume,
                'description' : product.description,
                'summary'     : product.summary,
                'price'       : product.price,
                'stock'       : product.stock,
                'images'      : [image.image_url for image in product.picture_set.all()]  
            }

            return JsonResponse({'product_detail' : product_detail} , status = 200)
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_PRODUCT_ID'} , status = 404)