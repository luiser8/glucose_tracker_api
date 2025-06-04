from marshmallow import Schema, fields, validate

class HbA1cSchema(Schema):
    actual_glucose = fields.Float(required=True, validate=validate.Range(min=0))
    objective_glucose = fields.Float(required=True, validate=validate.Range(min=0))
    carbohydrates = fields.Float(required=True, validate=validate.Range(min=0))