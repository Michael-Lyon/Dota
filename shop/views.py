from itertools import product
from zoneinfo import available_timezones

from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm

from .models import Category, Products

from .recommender import Recommender



def landing(request):
    return render(request, "store/landing.html")



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Products.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'store/home.html', {
    # return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def product_detail(request,id, slug):
    product = get_object_or_404(Products,id=id, slug=slug, available=True)
    r = Recommender()
    # recommended_products = r.suggest_product_for([product], 1)
    recommended_products = False
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/single.html', {'product':product, 'cart_product_form': cart_product_form, 'recommended_products': recommended_products})