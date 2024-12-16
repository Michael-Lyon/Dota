from http import client
from io import BytesIO
import os
from django.contrib.staticfiles import finders

import braintree
import xhtml2pdf.pisa as pisa
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from orders.models import Order


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        # Create and submit transaction
        result = braintree.Transaction.sale({
            'amount': round(order.get_total_cost(), 2),
            'payment_method_nonce': nonce,
            'options':{
                'submit_for_settlement':True
            }
        })
        if result.is_success:
            #mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # create and send invoice to the customer
            subject = f'NilexGlobalSolar - Invoice no. {order.id}'
            message = f"Please, find the attached invoice for your recent purchase."
            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [order.email]
            )
            # generate PDF
            html = render_to_string('orders/order/pdf.html', {'order': order})
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            
            # ATTACH PDF file
            # email.attach(f'order_{order.id}.pdf', response.getvalue(), 'application/pdf')
            #send mail
            # email.send()
            return response
            # return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # Generate token
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        return result[0]
    return None
