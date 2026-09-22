from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)

  products = db.relationship(
      "Product",
      backref="seller",
      lazy=True,
      cascade="all, delete-orphan",
  )

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)


class Product(db.Model):
  __tablename__ = "products"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150), nullable=False)
  price = db.Column(db.Float, nullable=False)
  stock = db.Column(db.Integer, nullable=False)

  seller_id = db.Column(
      db.Integer, db.ForeignKey("users.id"), nullable=False
  )