from django.urls import path

from products.views import *

urlpatterns = [
    path('/categories/<int:category_id>',CategoryView.as_view()),
    path('/categories/<int:category_id>/products/<int:product_id>',ProductView.as_view())
]