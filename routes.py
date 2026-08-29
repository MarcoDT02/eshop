from flask import Blueprint, request, jsonify
from models import db, User, Product

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists."}), 400

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!", "user_id": new_user.id}), 201


@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials."}), 401

    return jsonify({
        "message": "Login successful!",
        "user_id": user.id,
        "username": user.username
    }), 200


@api_bp.route("/products", methods=["POST"])
def add_product():
    data = request.get_json() or {}

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")
    seller_id = data.get("seller_id")

    if not name or price is None or stock is None or seller_id is None:
        return jsonify({"error": "Missing fields (name, price, stock, seller_id)."}), 400

    seller = User.query.get(seller_id)
    if not seller:
        return jsonify({"error": "Seller not found."}), 404

    try:
        new_product = Product(
            name=name,
            price=float(price),
            stock=int(stock),
            seller_id=int(seller_id)
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "message": "Product added successfully!",
            "product": new_product.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    products_list = [p.to_dict() for p in products]

    return jsonify({
        "count": len(products_list),
        "products": products_list
    }), 200