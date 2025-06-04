from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    firstname = fields.String(required=True, validate=validate.Length(min=3, max=100))
    lastname = fields.String(required=True, validate=validate.Length(min=3, max=100))
    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Length(min=3, max=100))


class ChangePasswordSchema(Schema):
    code = fields.String(required=True, validate=validate.Length(min=3, max=16))
    email = fields.String(required=True, validate=validate.Email())
    newpassword = fields.String(required=True, validate=validate.Length(min=3, max=100))
