
from typing import Dict, Optional, List
from database.db_operarions import DbManager
from models.event import DiaryEvent
from dateutil.parser import parse


class DiaryEventDb:
    table_name = 'events'

    @classmethod
    def get_all(cls) -> List[DiaryEvent]:
        query = "SELECT * FROM {table}".format(table=cls.table_name)
        result = DbManager.execute_query(query)
        events = []
        for row in result.fetchall():
            events.append(DiaryEvent(row['id'], row['title'], row['description'], parse(row['date'])))
        return events

    @classmethod
    def get(cls, event_id: int) -> Optional[DiaryEvent]:
        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.table_name)
        result = DbManager.execute_query_with_params(query, (event_id,))
        row = result.fetchone()
        if row:
            return DiaryEvent(row['id'], row['title'], row['description'], parse(row['date']))

    @classmethod
    def add(cls, event: DiaryEvent) -> DiaryEvent:
        query = "INSERT INTO {table}(title,description,date) values (?,?,?)".format(table=cls.table_name)
        result = DbManager.execute_query_with_params(query, (event.title, event.description, event.date))

        return DiaryEvent(result.lastrowid, event.title, event.description, event.date)

    @classmethod
    def update(cls, updated_event: DiaryEvent) -> DiaryEvent:
        query = "UPDATE {table} SET title=?, description=?,date=?" \
                "WHERE id =?".format(table=cls.table_name)
        DbManager.execute_query_with_params(query, (
            updated_event.title, updated_event.description, updated_event.date, updated_event.id))

        return DiaryEventDb.get(updated_event.id)


