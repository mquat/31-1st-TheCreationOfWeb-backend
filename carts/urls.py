from django.urls import path

from carts.views import CartListView

urlpatterns = [
    path('', CartListView.as_view()),
    path('/<int:cart_id>', CartListView.as_view()),
]