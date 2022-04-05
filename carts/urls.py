from django.urls import path

from carts.views import CartListView, CartPriceView

urlpatterns = [
    path('', CartListView.as_view()),
    path('/<int:cart_id>', CartPriceView.as_view()),
]