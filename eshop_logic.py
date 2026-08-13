import json
import os

FILENAME = "shop-data.json"

def loaddata():
    try:
        if os.path.exists(FILENAME):
            with open(FILENAME, "r") as data_file:
                return json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {"products": [], "cart": []}

def savedata(data):
    with open(FILENAME, "w") as data_file:
        json.dump(data, data_file, indent=4)

class EShop:
    def __init__(self):
        data = loaddata()
        self.products = data.get("products", [])
        self.cart = data.get("cart", [])

    def add_to_products(self, name, price, stock):
        new_product = {
            "id": len(self.products) + 1,
            "name": name,
            "price": float(price),
            "stock": int(stock)
        }
        self.products.append(new_product)
        savedata({
            "products": self.products,
            "cart": self.cart
        })
        return new_product

    def get_products(self):
        return self.products