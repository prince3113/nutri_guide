from marshmallow import Schema, fields, validate

class HealthProfileSchema(Schema):
    age = fields.Int(required=True)
    gender = fields.Str(required=True)
    height = fields.Float(required=True)
    weight = fields.Float(required=True)
    activity_level = fields.Str(required=True)
    goal = fields.Str(required=True)
    diet_type = fields.Str(required=True, validate=validate.OneOf(["vegetarian", "non-vegetarian"]))