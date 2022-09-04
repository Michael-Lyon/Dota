from itertools import product
import json
from statistics import quantiles

import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from python_paystack.managers import TransactionsManager
from python_paystack.objects.transactions import Transaction
from django.contrib.sites.shortcuts import get_current_site
from cart.cart import Cart
from coupons.forms import CouponApplyForm

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    coupon_form = CouponApplyForm()
    form = OrderCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
                order.country = request.POST.get('country')
            

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
            order.save()
            # clear the cart
            cart.clear()

           # launch asynchronous task
            request.session['order_id'] = order.id
            # order_created.delay(order.id)
            # set the order in the session
            # redirect for payment
            if request.POST.get('paymentMethod') == 'bt':
                order.save()
                return redirect(reverse('payment:process'))
            else:
                email = request.user.email
                callback = f"{get_current_site(request)}:{reverse('shop:product_list')}"
                print(callback)
                fee = order.get_total_cost() * 100
                transaction = Transaction(fee, email)
                transaction_manager = TransactionsManager()
                transaction = transaction_manager.initialize_transaction(
                    'STANDARD', transaction, callback_url=callback)  # TODO callback_url=callback)
                payment_info = json.loads(transaction.to_json())
                order.paystack_reference = payment_info['reference']
                order.save()
                return redirect(transaction.authorization_url)

    else:
        return render(request,
                      'orders/order/checkout.html',
                      {'cart': cart, 'form': form, 'coupon_form': coupon_form})


# TODO:You can also modify the admin order detail template and the order PDF bill to display the applied coupon the same way we did for the cart.
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\
                "order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(f"{settings.STATIC_ROOT}/css/pdf.css")])
    return response
