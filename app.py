from flask import Flask, jsonify, request
from eshop_logic import EShopDB

app = Flask(__name__)

shop = EShopDB(db_name="eshop", db_user="postgres", db_password="PASSWORD") # change PASSWORD -----------------------------------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"success": False, "error": "Missing username or password"}), 400

    result = shop.register_user(data["username"], data["password"])
    if result["success"]:
        return jsonify({"success": True, "message": "User registered successfully!", "user_id": result["user_id"]}), 201
    return jsonify({"success": False, "error": result["error"]}), 400

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"success": False, "error": "Missing username or password"}), 400

    result = shop.login_user(data["username"], data["password"])
    if result["success"]:
        return jsonify({"success": True, "message": "Login successful!", "user_id": result["user_id"]}), 200
    return jsonify({"success": False, "error": result["error"]}), 401

@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No JSON data provided."}), 400

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")
    seller_id = data.get("seller_id")

    if not name or price is None or stock is None or seller_id is None:
        return jsonify({"success": False, "error": "Missing fields (name, price, stock, seller_id)."}), 400

    try:
        product = shop.add_to_products(name, float(price), int(stock), int(seller_id))
        return jsonify({"success": True, "message": "Product added successfully!", "product": product}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/products", methods=["GET"])
def get_products():
    products = shop.get_products()
    return jsonify({"success": True, "count": len(products), "products": products}), 200

if __name__ == "__main__":
    app.run(debug=True)