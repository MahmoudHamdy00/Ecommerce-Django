import imp
from multiprocessing import context
from django.shortcuts import render
from .models import Product
from Category.models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_view(request):
    path = request.get_full_path()
    currentCategoryName = request.GET.get('category', '')
    order = request.GET.get('order', 'created_at')
    Categories = Category.objects.all()
   # Categories2 = Categories.values_list('name', 'product__count')
    if(currentCategoryName):
        currentCategory = list(Category.objects.filter(
            name=currentCategoryName)).__getitem__(0).id
        Products = Product.objects.filter(
            category=currentCategory).order_by(order)
    else:
        Products = Product.objects.all().order_by(order)
    prodCount = Products.count
    if(path == '/'):
        path += '?'
    else:
        path += '&'
    print(currentCategoryName)
    print(order)

    page = request.GET.get('page', 1)

    paginator = Paginator(Products, 9)
    if(int(page) > paginator.num_pages):
        page = paginator.num_pages
    if(int(page) < 1):
        page = 1

    Products = paginator.page(page)

    print(page)
    print(currentCategoryName)
    context = {
        'products': Products,
        'categories': Categories,
        'prodCount': prodCount,
        'currentCategory': currentCategoryName,
        'path': path,
        'page': page,
        'totalPage': paginator.num_pages

    }
    return render(request, 'Product/products.html', context)


def product_details_view(request,_id):
    product = Product.objects.get(id=_id)
    Categories = Category.objects.all()
    currentCategory = Category.objects.get(id=product.category_id)

    print(currentCategory.name)
    context = {
        'product': product,
        'categories': Categories,
        'currentCategory': currentCategory.name
    }
    return render(request,'product/details.html',context)


def products_details_view(request):
    objects = Product.objects.all()
    context = {
        'objects': objects
    }
    return render(request, 'index.html', context)
    return render(request, 'product/details.html', context)
