from django.http  import JsonResponse
from django.views import View

from products.models import Product

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