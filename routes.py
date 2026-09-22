from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from models import Product, User, db
from schemas import ProductSchema, UserLoginSchema, UserRegisterSchema

api_bp = Blueprint("api", __name__, url_prefix="/api")

user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
product_schema = ProductSchema()
products_list_schema = ProductSchema(many=True)


@api_bp.route("/register", methods=["POST"])
def register():
  data = user_register_schema.load(request.get_json() or {})

  if User.query.filter_by(username=data["username"]).first():
    return (
        jsonify({
            "error": "Conflict",
            "message": "Username already exists.",
        }),
        409,
    )

  new_user = User(username=data["username"])
  new_user.set_password(data["password"])

  db.session.add(new_user)
  db.session.commit()

  return (
      jsonify({
          "message": "User registered successfully!",
          "user_id": new_user.id,
      }),
      201,
  )

@api_bp.route("/login", methods=["POST"])
def login():
  data = user_login_schema.load(request.get_json() or {})

  user = User.query.filter_by(username=data["username"]).first()

  if not user or not user.check_password(data["password"]):
    return (
        jsonify({
            "error": "Unauthorized",
            "message": "Invalid credentials.",
        }),
        401,
    )

  access_token = create_access_token(identity=str(user.id))

  return (
      jsonify({
          "message": "Login successful!",
          "access_token": access_token,
          "user_id": user.id,
          "username": user.username,
      }),
      200,
  )

@api_bp.route("/products", methods=["POST"])
@jwt_required()
def add_product():
  current_user_id = get_jwt_identity()

  data = product_schema.load(request.get_json() or {})

  new_product = Product(
      name=data["name"],
      price=data["price"],
      stock=data["stock"],
      seller_id=int(current_user_id),
  )

  db.session.add(new_product)
  db.session.commit()

  return (
      jsonify({
          "message": "Product created successfully!",
          "product": product_schema.dump(new_product),
      }),
      201,
  )

@api_bp.route("/products", methods=["GET"])
def get_products():
  products = Product.query.all()
  return (
      jsonify({
          "count": len(products),
          "products": products_list_schema.dump(products),
      }),
      200,
  )