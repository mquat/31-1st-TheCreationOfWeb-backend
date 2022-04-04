from django.views import View
from django.http  import JsonResponse

from products.models import *

class ProductListView(View):
    def get(self,request):
        try:
            category_id = request.GET.get('category_id' , None)
            page_id     = int(request.GET.get('page_id' , None))

            if category_id == None:
                return JsonResponse({'message' : 'QUERY_STRING_ERROR'} , status = 404)
            if page_id < 0:
                return JsonResponse({'message' : 'PAGE_NUMBER_ERROR'} , status = 404)

            PAGE_SIZE   = 10
            offset      = (page_id - 1) * PAGE_SIZE
            limit       = page_id * PAGE_SIZE

            products    = Product.objects.filter(category_id = category_id)[offset:limit]

            products_list = [{
                'id'     : product.id,
                'name'   : product.name,
                'price'  : product.price,
                'images' : [image.image_url for image in product.picture_set.all()]
            } for product in products]

            return JsonResponse({'product_list' : products_list} , status = 200)
        except ValueError:
            return JsonResponse({'message' : 'QUERY_STRING_ERROR'} , status = 404)
        except TypeError:
            return JsonResponse({'message' : 'QUERY_STRING_ERROR'} , status = 404)