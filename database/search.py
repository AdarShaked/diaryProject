from datetime import datetime
from typing import List

from database.db_operarions import DbManager
from models.event import DiaryEvent
from models.search import DiarySearch


class DiarySearchDb:
    _table_name = 'events'

    @classmethod
    def search(cls, search_obj: DiarySearch) -> List[DiaryEvent]:
        res = cls._get_search_result(search_obj)
        return DbManager.create_list_of_events_from_query_result(res)

    @classmethod
    def _get_search_result(cls, search_obj):
        # build query by parameters
        if search_obj.content:
            if search_obj.start_date and search_obj.end_date:
                return cls.search_by_content_and_dates(search_obj)

            return cls.search_by_content(search_obj.content)

        return cls.search_by_dates(search_obj.start_date, search_obj.end_date)

    @classmethod
    def search_by_content_and_dates(cls, search_obj: DiarySearch):
        query = "SELECT * FROM {table} WHERE description LIKE ? AND (date BETWEEN ? AND ?)".format(
            table=cls._table_name)
        return DbManager.execute_query_with_params(query,
                                                   ("%{content}%".format(content=search_obj.content),
                                                    search_obj.start_date, search_obj.end_date))

    @classmethod
    def search_by_content(cls, content: str):
        query = "SELECT * FROM {table} WHERE description LIKE ?".format(table=cls._table_name)

        return DbManager.execute_query_with_params(query, ("%{content}%".format(content=content),))

    @classmethod
    def search_by_dates(cls, start_date: datetime, end_date: datetime):
        query = "SELECT * FROM {table} WHERE  date BETWEEN ? AND ?".format(table=cls._table_name)
        return DbManager.execute_query_with_params(query,
                                                   (start_date, end_date))
