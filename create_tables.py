import sqlite3
from models.event import  DiaryEvent
from datetime import datetime
connection = sqlite3.connect('data.db')

cursor = connection.cursor()


create_table ="CREATE TABLE IF NOT EXISTS events ( id INTEGER PRIMARY KEY ,title TEXT,description TEXT,date TEXT)"

cursor.execute(create_table)
event = DiaryEvent(title="adar_event",description="this is just a description", date=datetime(2019,1,1))
add_event="INSERT INTO events(title,description,date) values (?,?,?)"
cursor.execute(add_event,(event.title,event.description,event.date))
connection.commit()

connection.close()