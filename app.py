from flask import Flask, jsonify, request
from eshop_logic import EShop

app = Flask(__name__)
shop = EShop()

@app.route("/api/admin/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No JSON data provided."}), 400

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not name or price is None or stock is None:
        return jsonify({"success": False, "error": "Missing fields (name, price, stock)."}), 400

    try:
        product = shop.add_to_products(name, float(price), int(stock))
        return jsonify({"success": True, "message": "Product added successfully!", "product": product}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/admin/products", methods=["GET"])
def get_products():
    products = shop.get_products()
    return jsonify({"success": True, "count": len(products), "products": products}), 200

if __name__ == "__main__":
    app.run(debug=True)