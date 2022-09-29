from marshmallow import Schema, fields


class AnimalCreateSchema(Schema):
    color = fields.Str(required=True)
    high = fields.Float(required=True)
    is_fly = fields.Boolean(required=True)
    is_play_soccer = fields.Boolean(required=True)
    name = fields.Str(required=True)
    weight = fields.Float(required=True)


class AnimalUpdateSchema(Schema):
    color = fields.Str(required=False)
    high = fields.Float(required=False)
    is_fly = fields.Boolean(required=False)
    is_play_soccer = fields.Boolean(required=False)
    name = fields.Str(required=False)
    weight = fields.Float(required=False)
