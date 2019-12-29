from typing import List

from flask import Response
from datetime import datetime
from dateutil.parser import parse

from models.event import DiaryEvent
from tests.test_crud_operations import add_events_to_db


def test_search_parms(client, app):
    with app.app_context():
        response: Response = client.get("/api/search")
        assert response.status_code == 400
        assert response.is_json == True

        response: Response = client.get("/api/search?wrong_param=haha")
        assert response.status_code == 400
        assert response.is_json == True

        response: Response = client.get("/api/search?content=somthing&start_date=2012-10-04T00:00:00")
        assert response.status_code == 400
        assert response.is_json == True
        assert response.get_json()["error"] == "invalid parameters ,the input should be range of dates(start and end)"

        response: Response = client.get("/api/search?content=somthing&end_date=2012-10-04T00:00:00")
        assert response.status_code == 400
        assert response.is_json == True
        assert response.get_json()["error"] == "invalid parameters ,the input should be range of dates(start and end)"


def insert_search_test_case_events_to_db() -> List[DiaryEvent]:
    events_list: List[DiaryEvent] = []
    events_list.append(DiaryEvent(title="adar birthday", description="big party", date=datetime(1992, 9, 7)))
    events_list.append(DiaryEvent(title="bob birthday", description="beer party", date=datetime(2019, 12, 30)))
    events_list.append(DiaryEvent(title="new year party", description="party all night", date=datetime(2019, 12, 31)))
    add_events_to_db(events_list)
    return events_list


def test_search_by_content(client, app):
    with app.app_context():
        events_list: List[DiaryEvent] = insert_search_test_case_events_to_db()

        response: Response = client.get("/api/search?content=big")
        assert response.status_code == 200
        assert response.is_json == True

        events = response.get_json()['events']

        assert len(events) == 1
        assert events[0]['title'] == events_list[0].title
        assert parse(events[0]['date']) == events_list[0].date
        assert events[0]['description'] == events_list[0].description

        response: Response = client.get("/api/search?content=party")
        assert response.status_code == 200
        assert response.is_json == True
        events = response.get_json()['events']
        assert len(events) == 3
        assert events[0]['title'] == events_list[0].title
        assert parse(events[0]['date']) == events_list[0].date
        assert events[0]['description'] == events_list[0].description
        assert events[1]['title'] == events_list[1].title
        assert parse(events[1]['date']) == events_list[1].date
        assert events[1]['description'] == events_list[1].description
        assert events[2]['title'] == events_list[2].title
        assert parse(events[2]['date']) == events_list[2].date
        assert events[2]['description'] == events_list[2].description

        response: Response = client.get("/api/search?content=boom")
        assert response.status_code == 200
        assert response.is_json == True
        events = response.get_json()['events']
        assert len(events) == 0


def test_search_by_dates(client, app):
    with app.app_context():
        events_list: List[DiaryEvent] = insert_search_test_case_events_to_db()
        response: Response = client.get("/api/search?start_date=1992-09-07T00:00:00&end_date=2019-12-30T00:00:00")
        assert response.status_code == 200
        assert response.is_json == True

        events = response.get_json()['events']

        assert len(events) == 2
        assert events[0]['title'] == events_list[0].title
        assert parse(events[0]['date']) == events_list[0].date
        assert events[0]['description'] == events_list[0].description
        assert events[1]['title'] == events_list[1].title
        assert parse(events[1]['date']) == events_list[1].date
        assert events[1]['description'] == events_list[1].description

        response: Response = client.get("/api/search?start_date=1992-09-07T00:00:00&end_date=2019-12-29T00:00:00")
        assert response.status_code == 200
        assert response.is_json == True
        events = response.get_json()['events']
        assert len(events) == 1
        assert events[0]['title'] == events_list[0].title
        assert parse(events[0]['date']) == events_list[0].date
        assert events[0]['description'] == events_list[0].description

        response: Response = client.get("/api/search?start_date=1992-09-08T00:00:00&end_date=2019-12-29T00:00:00")
        assert response.status_code == 200
        assert response.is_json == True
        events = response.get_json()['events']
        assert len(events) == 0


def test_search_by_dates_and_content(client, app):
    with app.app_context():
        events_list: List[DiaryEvent] = insert_search_test_case_events_to_db()

        response: Response = client.get(
            "/api/search?content=big&start_date=1992-09-07T00:00:00&end_date=2019-12-30T00:00:00")
        assert response.status_code == 200
        assert response.is_json == True
        events = response.get_json()['events']
        assert len(events) == 1
        assert events[0]['title'] == events_list[0].title
        assert parse(events[0]['date']) == events_list[0].date
        assert events[0]['description'] == events_list[0].description

        response: Response = client.get(
            "/api/search?content=party&start_date=1992-09-07T00:00:00&end_date=2019-12-30T00:00:00")
        assert response.status_code == 200
        assert response.is_json == True
        events = response.get_json()['events']
        assert len(events) == 2
        assert events[0]['title'] == events_list[0].title
        assert parse(events[0]['date']) == events_list[0].date
        assert events[0]['description'] == events_list[0].description
        assert events[1]['title'] == events_list[1].title
        assert parse(events[1]['date']) == events_list[1].date
        assert events[1]['description'] == events_list[1].description

        response: Response = client.get(
            "/api/search?content=night&start_date=2019-11-30T00:00:00&end_date=2019-12-30T00:00:00")
        assert response.status_code == 200
        assert response.is_json == True
        events = response.get_json()['events']
        assert len(events) == 0
