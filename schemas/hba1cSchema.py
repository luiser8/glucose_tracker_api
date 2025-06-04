from marshmallow import Schema, fields, validate

class HbA1cSchema(Schema):
    actual_glucose = fields.Integer(required=True, validate=validate.Range(min=0, max=1000))
    objective_glucose = fields.Integer(required=True, validate=validate.Range(min=70, max=120))
    carbohydrates = fields.Integer(required=True, validate=validate.Range(min=0, max=1000))