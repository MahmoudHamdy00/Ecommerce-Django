from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render
from Products.models import Product
from Category.models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    if not request.session['cart']:
            request.session['cart'] = "{}"
    return HttpResponse('<a href="Product">Go To Products</a>')
