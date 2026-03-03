import requests
import pandas as pd

# Load local price database
price_db = pd.read_csv("product_prices.csv")


# ---------------- PRICE LOOKUP ----------------
def get_price(product_name):
    product_name = product_name.lower()

    for _, row in price_db.iterrows():
        if row["name"].lower() in product_name:
            return int(row["price"])

    return 50   # default if not found


# ---------------- GENERIC FETCH FUNCTION ----------------
def fetch_from_open_api(barcode, url):
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("status") == 1:
            product = data.get("product", {})

            name = product.get("product_name", "Unknown Product")
            brand = product.get("brands", "")

            price = get_price(name)

            return {
                "name": f"{name} ({brand})",
                "price": price
            }

    except:
        pass

    return None


# ---------------- MAIN FUNCTION ----------------
def get_product_from_api(barcode):

    # 1️⃣ OpenFoodFacts
    product = fetch_from_open_api(
        barcode,
        f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    )
    if product:
        return product

    # 2️⃣ OpenBeautyFacts
    product = fetch_from_open_api(
        barcode,
        f"https://world.openbeautyfacts.org/api/v0/product/{barcode}.json"
    )
    if product:
        return product

    # 3️⃣ OpenPetFoodFacts
    product = fetch_from_open_api(
        barcode,
        f"https://world.openpetfoodfacts.org/api/v0/product/{barcode}.json"
    )
    if product:
        return product

    return None