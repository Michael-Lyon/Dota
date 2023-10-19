import os
from dotenv import load_dotenv
from myshop.settings import BASE_DIR
load_dotenv(os.path.join(BASE_DIR, ".env"))
import requests
from decimal import Decimal
from .models import Order


SECRET = os.getenv("PAYSTACK_SECRET")
PUBLIC = os.getenv("PAYSTACK_PUBLIC")
CALL_BACK = os.getenv("CALLBACK_URL")
secret_key = SECRET
headers = {
    "Authorization": f"Bearer {secret_key}",
    "Content-Type": "application/json"
}

def initialize_transaction(order_id):
    order = Order.objects.get(id=order_id)
    fee = order.get_total_cost() * Decimal('100')
    fee_str = str(fee)
    url = "https://api.paystack.co/transaction/initialize/"

    data = {
        "email": order.email,
        "amount": fee_str,
        "callback_url": CALL_BACK
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        data = data["data"]
        return data["authorization_url"], data["reference"]
    else:
        return False, None



def verify_transaction(reference):
    url=f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["status"]
