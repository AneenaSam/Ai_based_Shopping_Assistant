from cart import view_cart, get_total
from datetime import datetime
import random

STORE_NAME = "SmartCart AI Mart"
STORE_ADDRESS = "ShoppingGPT Street, Kochi"
GST_PERCENT = 5


def generate_bill():

    items = view_cart()

    if not items:
        return "Cart is empty"

    bill_no = random.randint(1000, 9999)
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    subtotal = get_total()
    gst = round(subtotal * GST_PERCENT / 100, 2)
    grand_total = round(subtotal + gst, 2)

    bill = f"""
🧾 {STORE_NAME}
{STORE_ADDRESS}
----------------------------------------
Bill No : {bill_no}
Date    : {now}
----------------------------------------
Item                Qty     Price     Total
----------------------------------------
"""

    for name, details in items.items():
        qty = details["quantity"]
        price = details["price"]
        total = qty * price

        bill += f"{name[:18]:18} {qty:<7} ₹{price:<8} ₹{total}\n"

    bill += f"""
----------------------------------------
Subtotal : ₹{subtotal}
GST ({GST_PERCENT}%) : ₹{gst}
----------------------------------------
Grand Total : ₹{grand_total}
----------------------------------------

✨ Thank you for shopping with us! ✨
"""

    return bill