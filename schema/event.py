from marshmallow import Schema, fields, post_load
from models.event import DiaryEvent


class DiaryEventSchema(Schema):
    id = fields.Integer(min=0)
    title = fields.String(required=True)
    description = fields.String(required=True)
    date = fields.DateTime(required=True)

    @post_load
    def make_diary_event(self, data, **kwargs):
        return DiaryEvent(**data)
