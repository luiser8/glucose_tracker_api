from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    firstname = fields.String(required=True, validate=validate.Length(min=3, max=100))
    lastname = fields.String(required=True, validate=validate.Length(min=3, max=100))
    email = fields.String(required=True, validate=validate.Email())
    phone = fields.String(required=False, validate=validate.Length(min=3, max=20))
    password = fields.String(required=True, validate=validate.Length(min=3, max=100))
    sex = fields.String(required=True, validate=validate.Length(min=1, max=10))
    address = fields.String(required=True, validate=validate.Length(min=3, max=100))
    date_of_birth = fields.String(required=True, validate=validate.Length(min=3, max=100))
    country = fields.String(required=True, validate=validate.Length(min=3, max=100))
    city = fields.String(required=True, validate=validate.Length(min=3, max=100))

class ChangePasswordSchema(Schema):
    code = fields.String(required=True, validate=validate.Length(min=3, max=16))
    email = fields.String(required=True, validate=validate.Email())
    newpassword = fields.String(required=True, validate=validate.Length(min=3, max=100))
