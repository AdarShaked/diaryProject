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
