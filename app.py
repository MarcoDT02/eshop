from flask import Flask
from models import db
from routes import api_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:PASSWORD@localhost:5432/eshop_db" # Change PASSWORD ----------------
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(api_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)