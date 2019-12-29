from typing import Optional, List
from dateutil.parser import parse

from database.db_operarions import DbManager
from models.event import DiaryEvent


class DiaryEventDb:
    _events_table_name = 'events'

    @classmethod
    def get_all(cls) -> List[DiaryEvent]:
        query = "SELECT * FROM {table}".format(table=cls._events_table_name)
        result = DbManager.execute_query(query)
        return DbManager.create_list_of_events_from_query_result(result)

    @classmethod
    def get(cls, event_id: int) -> Optional[DiaryEvent]:
        query = "SELECT * FROM {table} WHERE id=?".format(table=cls._events_table_name)
        result = DbManager.execute_query_with_params(query, (event_id,))
        row = result.fetchone()
        if row:
            return DiaryEvent(row['id'], row['title'], row['description'], parse(row['date']))

    @classmethod
    def add(cls, event: DiaryEvent) -> DiaryEvent:
        query = "INSERT INTO {table}(title,description,date) values (?,?,date(?))".format(table=cls._events_table_name)
        result = DbManager.execute_query_with_params(query, (event.title, event.description, event.date))

        return DiaryEvent(result.lastrowid, event.title, event.description, event.date)

    @classmethod
    def update(cls, updated_event: DiaryEvent) -> DiaryEvent:
        query = "UPDATE {table} SET title=?, description=?,date=?" \
                "WHERE id =?".format(table=cls._events_table_name)
        DbManager.execute_query_with_params(query, (
            updated_event.title, updated_event.description, updated_event.date, updated_event.id))

        return DiaryEventDb.get(updated_event.id)

    @classmethod
    def delete(cls, event_id: int):
        query = "DELETE FROM {table} WHERE id=?".format(table=cls._events_table_name)
        DbManager.execute_query_with_params(query, (event_id,))
