from django.views import View
from django.http  import JsonResponse

from products.models import *

class ProductListView(View):
    def get(self,request):
        category_id = int(request.GET.get('category_id' , None))
        offset = request.GET.get('offset' , None)
        limit = request.GET.get('limit' , None)

        if category_id <= 0:
            return JsonResponse({'message' : 'INVALID_CATEGORY_ID'} , status = 404)

        # offset      = (page_id - 1) * PAGE_SIZE
        # limit       = page_id * PAGE_SIZE

        products    = Product.objects.filter(category_id = category_id)#[offset:limit]

        products_list = [{
            'id'     : product.id,
            'name'   : product.name,
            'price'  : product.price,
            'images' : [image.image_url for image in product.picture_set.all()]
        } for product in products]

        return JsonResponse({'product_list' : products_list} , status = 200)