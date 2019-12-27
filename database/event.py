from datetime import datetime
from typing import Dict, Optional, List
import sqlite3
from database.db_operarions import DbManager
from models.event import DiaryEvent
from dateutil.parser import parse


class DiaryEventDb:
    @staticmethod
    def get_all() -> List[DiaryEvent]:
        query = "SELECT * FROM events"
        result = DbManager.execute_query(query)
        events = []
        for row in result.fetchall():
            print(dict(row))
            events.append(DiaryEvent(row['id'], row['title'], row['description'], parse(row['date'])))

        return events
