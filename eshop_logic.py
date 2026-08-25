import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash


class EShopDB:
    def __init__(self, db_name, db_user, db_password, db_host="localhost", db_port="5432"):
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        self.conn.autocommit = True

    def register_user(self, username, password):
        cursor = self.conn.cursor()
        try:
            password_hash = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id;",
                (username, password_hash)
            )
            user_id = cursor.fetchone()[0]
            return {"success": True, "user_id": user_id}
        except psycopg2.errors.UniqueViolation:
            return {"success": False, "error": "Username already exists."}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            cursor.close()

    def login_user(self, username, password):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s;", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password_hash'], password):
            return {"success": True, "user_id": user['id'], "username": user['username']}
        return {"success": False, "error": "Invalid credentials."}

    def add_to_products(self, name, price, stock, seller_id):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "INSERT INTO products (name, price, stock, seller_id) VALUES (%s, %s, %s, %s) RETURNING *;",
            (name, price, stock, seller_id)
        )
        new_product = cursor.fetchone()
        cursor.close()

        new_product['price'] = float(new_product['price'])
        return new_product

    def get_products(self):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM products;")
        products = cursor.fetchall()
        cursor.close()

        for p in products:
            p['price'] = float(p['price'])
        return products