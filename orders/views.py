from email.message import EmailMessage
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
            order.save()
            
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
            # clear the cart
            cart.clear()

           # launch asynchronous task
            request.session['order_id'] = order.id
            # TODO: order_created.delay(order.id)
            # set the order in the session
            # redirect for payment
            if request.POST.get('paymentMethod') == 'bt':
                return redirect(reverse('payment:process'))
            else:
                email = order.email
                callback = f"{get_current_site(request)}:{reverse('shop:product_list')}"
                print(callback)
                fee = order.get_total_cost() * 100
                transaction = Transaction(fee, email)
                transaction_manager = TransactionsManager()
                transaction = transaction_manager.initialize_transaction(
                    'STANDARD', transaction)  # TODO callback_url=callback)
                payment_info = json.loads(transaction.to_json())
                request.session['paystack_reference'] = payment_info['reference']
                order.paystack_reference = payment_info['reference']
                order.save()
                return redirect(transaction.authorization_url)
    else:
        if request.session.get('paystack_reference', None):
            order_id = request.session.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            transaction_manager = TransactionsManager()
            transaction = transaction_manager.verify_transaction(
                transaction_reference=request.session.get('paystack_reference'))
            payment_info = json.loads(transaction.to_json())
            # print(payment_info)
            if payment_info['status'] == "success":
                order.paid = True
                order.save()
                # create and send invoice to the customer
                subject = f'PyGod - Store - Invoice no. {order.id}'
                message = f"Please, find the attached invoice for your recent purchase."
                # email = EmailMessage(
                #     subject,
                #     message,
                #     settings.EMAIL_HOST_USER,
                #     [order.email]
                # )
                # generate PDF
                html = render_to_string('orders/order/pdf.html', {'order': order})
                # out = BytesIO()
                response = HttpResponse(content_type='application/pdf')
                stylesheets = [weasyprint.CSS(f"{settings.STATIC_ROOT}/css/pdf.css")]
                weasyprint.HTML(string=html).write_pdf(response,  # out
                                                    stylesheets=stylesheets)

                # ATTACH PDF file
                # email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
                #send mail
                # email.send()
                del request.session['paystack_reference']
                return response
            else:
                del request.session['paystack_reference']
                return redirect('payment:canceled')
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
