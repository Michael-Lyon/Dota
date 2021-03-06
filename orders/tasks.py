from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from myshop.settings import EMAIL_HOST_USER

@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """


    order = Order.objects.get(id=order_id)
    subject = f"Order {order_id}"
    message = f"Dear {order.first_name},\n\n\tYou have successfully placed an order. On MOMA&DOTA Frozen foods. Your order id is {order.id}"

    mail_sent = send_mail(subject, message, EMAIL_HOST_USER, [order.email])

    return mail_sent