from datetime import datetime


class DiarySearch:
    content: str
    start_date: datetime
    end_date: datetime

    def __init__(self, content: str = None, start_date: datetime = None, end_date: datetime = None):
        self.content = content
        self.start_date = start_date
        self.end_date = end_date
