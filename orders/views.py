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
from orders.payment_manage import initialize_transaction, verify_transaction
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
                transaction_url, reference = initialize_transaction(order.id)
                if transaction_url:
                    request.session['paystack_reference'] = reference
                    order.paystack_reference = reference
                    order.save()
                    return redirect(transaction_url)
                else:
                    return redirect('payment:canceled')
    else:
        trxref = request.GET.get('trxref', None)
        if trxref:
            order_id = request.session.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            transaction = verify_transaction(trxref)

            # print(payment_info)
            if transaction:
                order.paid = True
                order.save()
                # create and send invoice to the customer
                subject = f'NilexGlobalSolar - Invoice no. {order.id}'
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