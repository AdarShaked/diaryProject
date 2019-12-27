import os
from datetime import datetime
import unittest
from unittest import TestCase
from dateutil.parser import parse
from flask import Response

from app import create_app
from db import init_db, get_db
from models.event import DiaryEvent


class BaseTest(TestCase):
    def setUp(self) -> None:
        if os.path.exists('test.db'):
            os.remove('test.db')

        app = create_app('test.db')

        with app.app_context():
            init_db()

    def tearDown(self) -> None:
        if os.path.exists('test.db'):
            os.remove('test.db')


class GetTest(BaseTest):
    def test_get_all(self):
        app = create_app('test.db')

        with app.app_context():
            db = get_db()
            event = DiaryEvent(title="adar_event", description="this is just a description", date=datetime(2019, 1, 1))
            add_event = "INSERT INTO events(title,description,date) values (?,?,?)"
            db.execute(add_event, (event.title, event.description, event.date))
            db.commit()

        with app.test_client() as client:
            response: Response = client.get("/api/event")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.is_json, True)

            events = response.get_json()['events']

            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]['title'], event.title)
            self.assertEqual(parse(events[0]['date']), event.date)


class PutTest(BaseTest):
    def test_get2_all(self):
        app = create_app('test.db')

        with app.app_context():
            db = get_db()
            event = DiaryEvent(title="adar_event", description="this is just a description", date=datetime(2019, 1, 1))
            add_event = "INSERT INTO events(title,description,date) values (?,?,?)"
            db.execute(add_event, (event.title, event.description, event.date))
            db.commit()

        with app.test_client() as client:
            response: Response = client.get("/api/event")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.is_json, True)

            events = response.get_json()['events']

            self.assertEqual(len(events), 1)


if __name__ == '__main__':
    unittest.main()
