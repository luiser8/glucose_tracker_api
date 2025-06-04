from marshmallow import Schema, fields, validate

class MeasurementsSchema(Schema):
    date = fields.String(required=True, validate=validate.Length(min=10, max=10))
    hour = fields.String(required=True, validate=validate.Length(min=2, max=10))
    value = fields.Integer(required=True, validate=validate.Range(min=0, max=1000))