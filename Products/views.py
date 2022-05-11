import imp
from multiprocessing import context
from django.shortcuts import render
from .models import Product
from Category.models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template.defaulttags import register


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


def product_view(request):
    path = request.get_full_path()
    currentCategoryName = request.GET.get('category', '')
    order = request.GET.get('order', 'created_at')
    Categories = Category.objects.all()
   # Categories2 = Categories.values_list('name', 'product__count')
    if(currentCategoryName):
        currentCategory = list(Category.objects.filter(name=currentCategoryName)).__getitem__(0).id
        Products = Product.objects.filter(category=currentCategory).order_by(order)
    else:
        Products = Product.objects.all().order_by(order)
    prodCount = Products.count
    if(path[-1] == '/'):
        path += '?'
    else:
        path += '&'

    page = request.GET.get('page', 1)
    allProd = Product.objects.all()
    NumberOfProductsInCategory = {}
    for cur in Categories:
        NumberOfProductsInCategory[cur.name] = allProd.filter(category=cur).count()
    paginator = Paginator(Products, 16)
    if(int(page) > paginator.num_pages):
        page = paginator.num_pages
    if(int(page) < 1):
        page = 1

    Products = paginator.page(page)
    context = {
        'products': Products,
        'categories': Categories,
        'prodCount': prodCount,
        'currentCategory': currentCategoryName,
        'path': path,
        'page': page,
        'totalPage': paginator.num_pages,
        'cnt': NumberOfProductsInCategory,
    }
    return render(request, 'Product/products.html', context)


def product_details_view(request, _id):
    product = Product.objects.get(id=_id)
    Categories = Category.objects.all()
    currentCategory = Category.objects.get(id=product.category_id)
    allProd = Product.objects.all()
    NumberOfProductsInCategory = {}
    for cur in Categories:
        NumberOfProductsInCategory[cur.name] = allProd.filter(
            category=cur).count()
    context = {
        'product': product,
        'categories': Categories,
        'currentCategory': currentCategory.name,
        'cnt': NumberOfProductsInCategory,

    }
    return render(request, 'product/details.html', context)


# def products_details_view(request):
#     objects = Product.objects.all()
#     context = {
#         'objects': objects
#     }
#     return render(request, 'index.html', context)
#     return render(request, 'product/details.html', context)
