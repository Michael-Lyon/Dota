from http import client
import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO



def payment_process(request):
    order_id = request.session.get('order_id')
    print(order_id)
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
        print(request)
        if result.is_success:
            #mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # create and send invoice to the customer
            subject = f'MOMA&DOTA - Invoice no. {order.id}'
            message = f"Please, find the attached invoice for your recent purchase."
            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [order.email]
            )
            # generate PDF
            html = render_to_string('orders/order/pdf.html', {'order': order})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(f"{settings.STATIC_ROOT}/css/pdf.css")]
            weasyprint.HTML(string=html).write_pdf(out,
                                                   stylesheets=stylesheets)

            # ATTACH PDF file
            email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
            #send mail
            email.send()
            return redirect('payment:done')
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
