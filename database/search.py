from datetime import datetime
from typing import List

from database.db_operarions import DbManager
from models.event import DiaryEvent
from models.search import DiarySearch


class DiarySearchDb:
    table_name = 'events'

    @classmethod
    def search(cls, search_obj: DiarySearch) -> List[DiaryEvent]:
        # build query by parameters
        if search_obj.content:
            if search_obj.start_date and search_obj.start_date:
                res = cls.search_by_content_and_dates(search_obj)
            else:
                res = cls.search_by_content(search_obj.content)
        else:
            res = cls.search_by_dates(search_obj.start_date, search_obj.end_date)

        return DbManager.create_list_of_events_from_query_result(res)

    @classmethod
    def search_by_content_and_dates(cls, search_obj: DiarySearch):
        query = "SELECT * FROM {table} WHERE description LIKE \'%{content}%\' AND (date BETWEEN ? AND ?)".format(
            table=cls.table_name, content=search_obj.content)
        return DbManager.execute_query_with_params(query,
                                                   (search_obj.start_date, search_obj.end_date))

    @classmethod
    def search_by_content(cls, content: str):
        query = "SELECT * FROM {table} WHERE description LIKE \'%{content}%\'".format(table=cls.table_name,
                                                                                      content=content)
        return DbManager.execute_query(query)

    @classmethod
    def search_by_dates(cls, start_date: datetime, end_date: datetime):
        query = "SELECT * FROM {table} WHERE  date BETWEEN ? AND ?".format(table=cls.table_name)
        return DbManager.execute_query_with_params(query,
                                                   (start_date, end_date))
