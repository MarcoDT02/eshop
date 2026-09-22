from errors import register_error_handlers
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from routes import api_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:PASSWORD@localhost:5432/eshop"  # Replace PASSWORD --------------------------------
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = (
    "8f3b2a9e4c1d6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a"
)

jwt = JWTManager(app)
db.init_app(app)

register_error_handlers(app, jwt=jwt)

app.register_blueprint(api_bp)

with app.app_context():
  db.create_all()

if __name__ == "__main__":
  app.run(debug=True)