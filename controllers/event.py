from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from schema.event import DiaryEventSchema
from database.event import DiaryEventDb
from models.event import DiaryEvent

diary = Blueprint('diary', __name__)


class DiaryController:
    @staticmethod
    @diary.route('/api/event', methods=['GET'])
    def get_all():
        schema = DiaryEventSchema()
        return jsonify({'events': schema.dump(DiaryEventDb.get_all(), many=True)})

    @staticmethod
    @diary.route('/api/event/<int:event_id>', methods=['GET'])
    def get_by_id(event_id: int):
        event = DiaryEventDb.get(event_id)
        if event is None:
            return jsonify({"error": "event not found"}), 404

        schema = DiaryEventSchema()
        return jsonify(schema.dump(DiaryEventDb.get(event_id)))

    @staticmethod
    @diary.route('/api/event', methods=['POST'])
    def add_event():
        try:
            if not request.is_json:
                return jsonify({"error": "please provide data in json format"}), 400

            schema = DiaryEventSchema()
            event: DiaryEvent = schema.load(request.json)

            if event.id is not None:
                return jsonify({"error": "cant put event with id"}), 400

            event_added = DiaryEventDb.add(event)
            return jsonify(schema.dump(event_added))

        except ValidationError as e:
            return jsonify({"error": e.messages}), 400

    # assumig that if the event doesent exsits its fault
    # assuming if the body dont have is event_id is from url
    @staticmethod
    @diary.route('/api/event/<int:event_id>', methods=['PUT'])
    def update_event(event_id: int):
        try:
            if not request.is_json:
                return jsonify({"error": "please provide data in json format"}), 400

            if DiaryEventDb.get(event_id) is None:
                return jsonify({"error": "event not found"}), 404

            schema = DiaryEventSchema()
            updated_event: DiaryEvent = schema.load(request.json)
            if updated_event.id is None:
                updated_event.id = event_id

            if updated_event.id != event_id:
                return jsonify({"error": "id conflict between url and body"}), 400

            return jsonify(schema.dump(DiaryEventDb.update(updated_event)))

        except ValidationError as e:
            return jsonify({"error": e.messages}), 400

    @staticmethod
    @diary.route('/api/event/<int:event_id>', methods=['DELETE'])
    def delete_event(event_id: int):
        event = DiaryEventDb.get(event_id)
        if event is None:
            return jsonify({"error": "event not found"}), 404
        DiaryEventDb.delete(event_id)
        # if we deleted succesfully - 204-no content
        return "", 204
