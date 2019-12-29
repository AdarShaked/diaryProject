from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from database.search import DiarySearchDb
from models.search import DiarySearch
from schema.event import DiaryEventSchema
from schema.search import SearchEventSchema

search = Blueprint('search', __name__)


class SearchController:

    # query string :/api/search?content=".."&start_date="<iso format date>"&end_date="<iso format date>"
    @staticmethod
    @search.route('/api/search', methods=['GET'])
    def search_events():
        try:
            if len(request.args) == 0:
                return jsonify({"error": "please provide a query string"}), 400

            search_schema = SearchEventSchema()
            search_obj: DiarySearch = search_schema.load(request.args)
            if (search_obj.start_date is None and search_obj.end_date) or (
                    search_obj.start_date and search_obj.end_date is None):
                return jsonify({"error": "invalid parameters ,the input should be range of dates(start and end)"}), 400

            event_schema = DiaryEventSchema()
            return jsonify({'events': event_schema.dump(DiarySearchDb.search(search_obj), many=True)})
        except ValidationError as e:
            return jsonify({"error": e.messages}), 400
