def test_register_success(client):
    response = client.post(
        "/api/register",
        json={"username": "newuser", "password": "password123"},
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "User registered successfully!"
    assert "user_id" in data


def test_register_duplicate_username(client):
    payload = {"username": "dupuser", "password": "password123"}
    client.post("/api/register", json=payload)

    response = client.post("/api/register", json=payload)
    data = response.get_json()

    assert response.status_code == 409
    assert data["error"] == "Conflict"


def test_register_validation_error(client):
    response = client.post(
        "/api/register",
        json={"username": "a", "password": "123"},
    )
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Validation Error"
    assert "details" in data


def test_login_success(client):
    client.post(
        "/api/register",
        json={"username": "loginuser", "password": "password123"},
    )

    response = client.post(
        "/api/login",
        json={"username": "loginuser", "password": "password123"},
    )
    data = response.get_json()

    assert response.status_code == 200
    assert "access_token" in data
    assert data["username"] == "loginuser"


def test_login_invalid_credentials(client):
    client.post(
        "/api/register",
        json={"username": "loginuser", "password": "password123"},
    )

    response = client.post(
        "/api/login",
        json={"username": "loginuser", "password": "wrongpassword"},
    )
    data = response.get_json()

    assert response.status_code == 401
    assert data["error"] == "Unauthorized"


def test_get_products_empty(client):
    response = client.get("/api/products")
    data = response.get_json()

    assert response.status_code == 200
    assert data["count"] == 0
    assert data["products"] == []


def test_add_product_success(client, auth_headers):
    response = client.post(
        "/api/products",
        json={"name": "Gaming Mouse", "price": 49.99, "stock": 10},
        headers=auth_headers,
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["product"]["name"] == "Gaming Mouse"
    assert data["product"]["price"] == 49.99
    assert data["product"]["stock"] == 10
    assert data["product"]["seller_id"] == 1


def test_add_product_missing_token(client):
    response = client.post(
        "/api/products",
        json={"name": "Gaming Mouse", "price": 49.99, "stock": 10},
    )
    data = response.get_json()

    assert response.status_code == 401
    assert data["error"] == "Authorization Required"


def test_add_product_invalid_token(client):
    response = client.post(
        "/api/products",
        json={"name": "Gaming Mouse", "price": 49.99, "stock": 10},
        headers={"Authorization": "Bearer invalid.token.string"},
    )
    data = response.get_json()

    assert response.status_code == 401
    assert data["error"] == "Invalid Token"


def test_get_products_after_creation(client, auth_headers):
    client.post(
        "/api/products",
        json={"name": "Monitor 27", "price": 250.0, "stock": 5},
        headers=auth_headers,
    )

    response = client.get("/api/products")
    data = response.get_json()

    assert response.status_code == 200
    assert data["count"] == 1
    assert data["products"][0]["name"] == "Monitor 27"