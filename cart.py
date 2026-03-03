cart = {}

def add_to_cart(product):

    name = product["name"]

    if name in cart:
        cart[name]["quantity"] += 1
    else:
        cart[name] = {
            "price": product["price"],
            "quantity": 1
        }

def view_cart():
    return cart

def get_total():
    return sum(item["price"] * item["quantity"] for item in cart.values())

def clear_cart():
    cart.clear()


# 🗑 REMOVE FULL PRODUCT
def remove_item_from_cart(product_name):

    if product_name in cart:
        del cart[product_name]
        return True

    return False