from flask import Blueprint,jsonify, request, Response
from werkzeug.exceptions import BadRequest, NotFound
from schema.event import DiaryEventSchema
from database.event import DiaryEventDb
diary = Blueprint('diary', __name__)


class DiaryController:
    @staticmethod
    @diary.route('/api/event', methods=['GET'])
    def get_all():
        schema = DiaryEventSchema()
        return jsonify({'events':schema.dump(DiaryEventDb.get_all(), many=True)})

    @staticmethod
    @diary.route('/api/event/<event_id>', methods=['GET'])
    def get_by_id(event_id:int):
        event = DiaryEventDb.get(event_id)
        if event is None:
            return NotFound('event not found')
        schema = DiaryEventSchema()
        return jsonify(schema.dump(DiaryEventDb.get(event_id)))


