from marshmallow import Schema, fields

class GigSchema(Schema):
    id = fields.Int(dump_only=True)
    website_supplied_id = fields.Str(required=False)
    name = fields.Str(required=False)
    url = fields.Str(required=False)
    location = fields.Str(required=False)
    datetime = fields.DateTime(required=False)
    details = fields.Str(required=False)
