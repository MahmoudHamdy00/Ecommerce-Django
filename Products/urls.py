from django.urls import path
from .views import product_details_view, product_view, add_to_cart, checkout, remove_from_cart

urlpatterns = [
    path('<int:_id>', product_details_view, name="product details"),
    path('', product_view, name="product details"),
    path('add_to_cart/<int:id>', add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:id>', remove_from_cart, name="remove_from_cart"),
    path('checkout', checkout, name="checkout")
]
