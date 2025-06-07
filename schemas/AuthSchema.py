from marshmallow import Schema, fields, validate

class AuthSchema(Schema):
    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Length(min=3, max=100))