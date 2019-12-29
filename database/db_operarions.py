import sqlite3
from typing import List
from dateutil.parser import parse

from db import get_db
from models.event import DiaryEvent


class DbManager:
    @staticmethod
    def execute_query(query):
        connection = get_db()
        cursor = connection.cursor()
        result = cursor.execute(query)
        connection.commit()
        return result

    @staticmethod
    def execute_query_with_params(query: str, args: tuple):
        connection = get_db()
        cursor = connection.cursor()
        result = cursor.execute(query, args)
        connection.commit()
        return result

    @staticmethod
    def create_list_of_events_from_query_result(result: sqlite3.Cursor) -> List[DiaryEvent]:
        events = []
        for row in result.fetchall():
            events.append(DiaryEvent(row['id'], row['title'], row['description'], parse(row['date'])))
        return events
