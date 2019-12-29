from marshmallow import Schema, fields, post_load
from models.search import DiarySearch


class SearchEventSchema(Schema):
    content = fields.String()
    start_date = fields.DateTime()
    end_date = fields.DateTime()

    @post_load
    def make_diary_search(self, data, **kwargs):
        return DiarySearch(**data)
