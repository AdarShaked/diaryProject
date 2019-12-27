from datetime import datetime
from typing import Dict, Optional, List
import sqlite3
from database.db_operarions import DbOperations
from models.event import DiaryEvent
from dateutil.parser import  parse


class DiaryEventDb:
    @staticmethod
    def get_all()->List[DiaryEvent]:
        query = "SELECT * FROM events"
        result,connection = DbOperations.connect_and_execute_query(query)
        events=[]
        for row in result.fetchall():
            print (dict(row))
            events.append(DiaryEvent(row['id'],row['title'],row['description'],parse(row['date'])))
        DbOperations.close_connection(connection)
        return events