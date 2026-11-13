import pytest
from marshmallow import ValidationError
from models import User
from schemas import ProductSchema, UserLoginSchema, UserRegisterSchema


def test_password_hashing():
    user = User(username="john_doe")
    user.set_password("secret123")

    assert user.password_hash != "secret123"
    assert user.check_password("secret123") is True
    assert user.check_password("wrongpass") is False


def test_user_register_schema_valid():
    schema = UserRegisterSchema()
    data = schema.load({"username": "validuser", "password": "password123"})

    assert data["username"] == "validuser"
    assert data["password"] == "password123"


def test_user_register_schema_invalid():
    schema = UserRegisterSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({"username": "ab", "password": "123"})

    errors = exc_info.value.messages
    assert "username" in errors
    assert "password" in errors


def test_user_login_schema_missing_fields():
    schema = UserLoginSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({})

    errors = exc_info.value.messages
    assert "username" in errors
    assert "password" in errors


def test_product_schema_valid():
    schema = ProductSchema()
    data = schema.load({"name": "Mechanical Keyboard", "price": 89.99, "stock": 15})

    assert data["name"] == "Mechanical Keyboard"
    assert data["price"] == 89.99
    assert data["stock"] == 15


def test_product_schema_invalid_values():
    schema = ProductSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({"name": "A", "price": 0, "stock": -5})

    errors = exc_info.value.messages
    assert "name" in errors
    assert "price" in errors
    assert "stock" in errors