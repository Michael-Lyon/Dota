from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.views.decorators.http import require_POST
from shop import recommender
from shop.models import Products
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
# from shop.recommender import Recommender

@require_POST
def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('productid')
        cart = Cart(request)
        product = get_object_or_404(Products, id=product_id)
        cart.add(
            product=product,
            quantity=int(request.POST.get('productqty')),
            update_quantity=request.POST.get('update', False)
        )
        qty = cart.__len__()
        return JsonResponse({"qty": qty, "subtotal": cart.get_total_price()})



@require_POST
def cart_remove(request):
    cart = Cart(request)
    product_id = request.POST.get('productid')
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    return JsonResponse({"qty": cart.__len__(), "subtotal": cart.get_total_price()})

def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm(request.POST or None)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
            'update': True
            }
        )
    # r = Recommender()
    cart_products = [item['product'] for item in cart]
    # recommended_products = r.suggest_product_for(cart_products,
    #                                           max_results=4)
    recommended_products = False
    return render(request, 'cart/summary.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form, 'recommended_products': recommended_products})
