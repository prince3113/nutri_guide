from marshmallow import Schema, fields

class HealthProfileSchema(Schema):
    age = fields.Int(required=True)
    gender = fields.Str(required=True)
    height = fields.Float(required=True)
    weight = fields.Float(required=True)
    activity_level = fields.Str(required=True)
    goal = fields.Str(required=True)