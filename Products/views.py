import ast
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


def add_to_cart(request, id):
    if not request.session['cart']:
        request.session['cart'] = "{}"

    # convert string to dictionary
    productsInCart = ast.literal_eval(request.session['cart'])
    # add product to products in cart
    if id in productsInCart:
        productsInCart[id] += 1
    else:
        productsInCart[id] = 1

    itemsCount = 0
    for k in productsInCart:
        itemsCount += productsInCart[k]
    request.session['cart'] = str(productsInCart)
    print(request.session['cart'])
    # stay at home page
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
    if(path[-1] == '/'):
        path += '?'
    else:
        path += '&'

    page = request.GET.get('page', 1)
    allProd = Product.objects.all()
    NumberOfProductsInCategory = {}
    for cur in Categories:
        NumberOfProductsInCategory[cur.name] = allProd.filter(
            category=cur).count()
    paginator = Paginator(Products, 16)
    if(int(page) > paginator.num_pages):
        page = paginator.num_pages
    if(int(page) < 1):
        page = 1

    Products = paginator.page(page)
    context = {
        'itemsCount': itemsCount,
        'products': Products,
        'categories': Categories,
        'prodCount': prodCount,
        'currentCategory': currentCategoryName,
        'path': '',
        'page': page,
        'totalPage': paginator.num_pages,
        'cnt': NumberOfProductsInCategory,
    }
    return render(request, 'Product/products.html', context)


def remove_from_cart(request, id):
    # convert string to dictionary
    productsInCart = ast.literal_eval(request.session['cart'])
    # remove product to products in cart
    if id in productsInCart:
        productsInCart.pop(id)
        # del productsInCart[id]

    ids = list(productsInCart.keys())
    itemsCount = 0
    for k in productsInCart:
        itemsCount += productsInCart[k]
    products = Product.objects.filter(id__in=ids)
    total = 0.0
    for pro in products:
        # pro.amount
        total += (float(pro.price))
        # print(type(productsInCart[int(pro.id)]))
    request.session['cart'] = str(productsInCart)
    NumberOfProductsInCategory = {}
    Categories = Category.objects.all()
    allProd = Product.objects.all()

    for cur in Categories:
        NumberOfProductsInCategory[cur.name] = allProd.filter(
            category=cur).count()
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'itemsCount': itemsCount,
        'total': total,
        'cnt': NumberOfProductsInCategory,

    }
    return render(request, 'Product/checkout.html', context)


def checkout(request):
    # go to check out page
    productsInCart = ast.literal_eval(request.session['cart'])
    ids = list(productsInCart.keys())
    print('------------')
    print(productsInCart)
    itemsCount = 0
    for k in productsInCart:
        itemsCount += productsInCart[k]
    products = Product.objects.filter(id__in=ids)
    total = 0.0
    for pro in products:
        # pro.amount
        total += (float(pro.price))
        # print(type(productsInCart[int(pro.id)]))

    path = request.get_full_path()
    Categories = Category.objects.all()

    prodCount = products.count
    if(path[-1] == '/'):
        path += '?'
    else:
        path += '&'

    page = request.GET.get('page', 1)
    allProd = Product.objects.all()
    NumberOfProductsInCategory = {}
    for cur in Categories:
        NumberOfProductsInCategory[cur.name] = allProd.filter(
            category=cur).count()
    paginator = Paginator(products, 16)
    if(int(page) > paginator.num_pages):
        page = paginator.num_pages
    if(int(page) < 1):
        page = 1

    products = paginator.page(page)
    productsInCart = ast.literal_eval(request.session['cart'])
    itemsCount = 0
    for k in productsInCart:
        itemsCount += productsInCart[k]
    context = {
        'itemsCount': itemsCount,
        'products': products,
        'categories': Categories,
        'prodCount': prodCount,
        'currentCategory': 'currentCategoryName',
        'path': path,
        'page': page,
        'totalPage': paginator.num_pages,
        'cartCount': itemsCount,
        'cnt': NumberOfProductsInCategory,
        'total': total
    }
    return render(request, 'Product/checkout.html', context)


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
    if(path[-1] == '/'):
        path += '?'
    else:
        path += '&'

    page = request.GET.get('page', 1)
    allProd = Product.objects.all()
    NumberOfProductsInCategory = {}
    for cur in Categories:
        NumberOfProductsInCategory[cur.name] = allProd.filter(
            category=cur).count()
    paginator = Paginator(Products, 16)
    if(int(page) > paginator.num_pages):
        page = paginator.num_pages
    if(int(page) < 1):
        page = 1

    Products = paginator.page(page)
    productsInCart = ast.literal_eval(request.session['cart'])
    itemsCount = 0
    for k in productsInCart:
        itemsCount += productsInCart[k]
    context = {
        'itemsCount': itemsCount,
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

    productsInCart = ast.literal_eval(request.session['cart'])
    itemsCount = 0
    for k in productsInCart:
        itemsCount += productsInCart[k]
    context = {
        'itemsCount': itemsCount,
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
