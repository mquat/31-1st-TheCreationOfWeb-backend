
from django.urls import path

from .views import CategoryView, ProductView 

urlpatterns =[
    path('/<int:category_id>', CategoryView.as_view()),
    path('/<int:category_id>/products/<int:product_id>',ProductView.as_view())
]