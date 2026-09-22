from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
  username = fields.String(
      required=True,
      validate=validate.Length(
          min=3,
          max=80,
          error="Username must be between 3 and 80 characters long.",
      ),
  )
  password = fields.String(
      required=True,
      validate=validate.Length(
          min=6, error="Password must be at least 6 characters long."
      ),
  )

class UserLoginSchema(Schema):
  username = fields.String(
      required=True,
      error_messages={"required": "The 'username' field is required."},
  )
  password = fields.String(
      required=True,
      error_messages={"required": "The 'password' field is required."},
  )

class ProductSchema(Schema):
  id = fields.Integer(dump_only=True)
  name = fields.String(
      required=True,
      validate=validate.Length(
          min=2,
          max=150,
          error="Product name must be between 2 and 150 characters long.",
      ),
  )
  price = fields.Float(
      required=True,
      validate=validate.Range(
          min=0.01, error="Price must be greater than 0.00."
      ),
  )
  stock = fields.Integer(
      required=True,
      validate=validate.Range(
          min=0, error="Stock cannot be a negative number."
      ),
  )
  seller_id = fields.Integer(dump_only=True)