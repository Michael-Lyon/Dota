from itertools import product
from zoneinfo import available_timezones
from django.shortcuts import render, get_object_or_404
from .models import Category, Products
from cart.forms import CartAddProductForm
from .recommender import Recommender

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Products.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def product_detail(request,id, slug):
    product = get_object_or_404(Products,id=id, slug=slug, available=True)
    r = Recommender()
    recommended_products = r.suggest_product_for([product], 4)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product':product, 'cart_product_form': cart_product_form, 'recommended_products': recommended_products})