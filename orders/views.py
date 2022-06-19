from itertools import product
from statistics import quantiles
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
                order.save()

            for item in cart:
                OrderItem.objects.create( order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # clear the cart
            cart.clear()

           # launch asynchronous task
            request.session['order_id'] = order.id
            order_created.delay(order.id)
            # set the order in the session
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart, 'form': form})


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
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
    return response
