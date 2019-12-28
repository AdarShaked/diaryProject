import pytest
import os
from datetime import datetime
from dateutil.parser import parse
from flask import Response, jsonify
import json

from db import init_db, get_db
from models.event import DiaryEvent


def add_event_to_db(event):
    db = get_db()
    add_event = "INSERT INTO events(title,description,date) values (?,?,?)"
    db.execute(add_event, (event.title, event.description, event.date))
    db.commit()


def test_get_all(client, app):
    with app.app_context():
        event = DiaryEvent(title="adar_event", description="this is just a description", date=datetime(2019, 1, 1))
        add_event_to_db(event)

    response: Response = client.get("/api/event")
    assert response.status_code == 200
    assert response.is_json == True

    events = response.get_json()['events']

    assert len(events) == 1
    assert events[0]['title'] == event.title
    assert parse(events[0]['date']) == event.date
    assert events[0]['description'] == event.description


def test_get_by_id(client, app):
    with app.app_context():
        event1 = DiaryEvent(title="adar_event", description="this is just a description",
                            date=datetime(2019, 1, 1))
        add_event_to_db(event1)
        event2 = DiaryEvent(title="adar_event2", description="this is just a description2",
                            date=datetime(2019, 1, 2))
        add_event_to_db(event2)

        response: Response = client.get("/api/event/1")
        assert response.status_code == 200
        assert response.is_json == True
        event = response.get_json()
        assert event['title'] == event1.title
        assert parse(event['date']) == event1.date
        assert event['description'] == event1.description

        response: Response = client.get("/api/event/2")
        assert response.status_code == 200
        assert response.is_json == True
        event = response.get_json()
        assert event['title'] == event2.title
        assert parse(event['date']) == event2.date
        assert event['description'] == event2.description

        response: Response = client.get("/api/event/3")
        assert response.status_code == 404


def test_put(client, app):
    with app.app_context():
        event_to_insert = DiaryEvent(title="post_event", description="this is just a description",
                                     date=datetime(2019, 1, 20))

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = {
            'title': event_to_insert.title,
            'description': event_to_insert.description,
            'date': str(event_to_insert.date)
        }
        response: Response = client.post("/api/event", json=data,headers=headers)
        assert response.status_code == 200
        assert response.is_json == True
        event_returned = response.get_json()
        assert event_returned['title'] == event_to_insert.title
        assert parse(event_returned['date']) == event_to_insert.date
        assert event_returned['description'] == event_to_insert.description
        assert event_returned["id"] == 1

        event_to_insert = DiaryEvent(title="post_event2", description="this is just a description2",
                                     date=datetime(2019, 2, 20))

        data = {
            'title': event_to_insert.title,
            'description': event_to_insert.description,
            'date': str(event_to_insert.date)
        }
        response: Response = client.post("/api/event", json=data, headers=headers)
        assert response.status_code == 200
        assert response.is_json == True
        event_returned = response.get_json()
        assert event_returned['title'] == event_to_insert.title
        assert parse(event_returned['date']) == event_to_insert.date
        assert event_returned['description'] == event_to_insert.description
        assert event_returned["id"] == 2

        #put bad requests
        data = {
            'title': event_to_insert.title,
            'description': event_to_insert.description,
            'date': str(event_to_insert.date),
            'id':5
        }
        response: Response = client.post("/api/event", json=data, headers=headers)
        assert response.status_code == 400
        assert response.is_json == True
        assert response.get_json()['error'] =="cant put event with id"


