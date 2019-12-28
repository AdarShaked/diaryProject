import pytest
import os
from datetime import datetime
from dateutil.parser import parse
from flask import Response
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
    assert parse(events[0]['date'])== event.date
    assert events[0]['description']== event.description

def test_get_by_id(client,app):

    with app.app_context():
        event1 = DiaryEvent(title="adar_event", description="this is just a description",
                            date=datetime(2019, 1, 1))
        add_event_to_db(event1)
        event2 = DiaryEvent(title="adar_event2", description="this is just a description2",
                            date=datetime(2019, 1, 2))
        add_event_to_db(event2)


        response: Response = client.get("/api/event/1")
        assert response.status_code== 200
        assert response.is_json== True
        event = response.get_json()
        assert event['title']== event1.title
        assert parse(event['date']) == event1.date
        assert event['description'] == event1.description

        response: Response = client.get("/api/event/2")
        assert response.status_code== 200
        assert response.is_json== True
        event = response.get_json()
        assert event['title']== event2.title
        assert parse(event['date'])== event2.date
        assert event['description']== event2.description

        response: Response = client.get("/api/event/3")
        print(response.status_code)
        assert response.status_code== 404