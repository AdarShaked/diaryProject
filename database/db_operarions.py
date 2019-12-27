import sqlite3


class DbOperations:
    db_name = "data.db"

    @staticmethod
    def connect_and_execute_query(query):
        connection = sqlite3.connect('data.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        result = cursor.execute(query)
        connection.commit()
        return result,connection

    @staticmethod
    def close_connection(connection):
        connection.close()