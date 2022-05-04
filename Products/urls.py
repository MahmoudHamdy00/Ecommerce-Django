from django.urls import path
from .views import product_details_view,product_view

urlpatterns = [
    path('<str:_id>', product_details_view, name="product details"),
    path('', product_view, name="product details"),
]
