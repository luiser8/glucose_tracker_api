from marshmallow import Schema, fields, validate

class ConfirmRegistrationSchema(Schema):
    email = fields.String(required=True, validate=validate.Email())
    code = fields.String(required=True, validate=validate.Length(min=4, max=6))