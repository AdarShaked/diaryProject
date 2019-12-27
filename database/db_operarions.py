import sqlite3

from db import get_db


class DbManager:
    @staticmethod
    def execute_query(query):
        connection = get_db()

        cursor = connection.cursor()
        result = cursor.execute(query)

        connection.commit()

        return result

