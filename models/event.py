from datetime import datetime


class DiaryEvent:
    id: int
    title: str
    description: str
    date: datetime

    def __init__(self, id: int = None, title: str = '', description: str = '', date: datetime = None):
        self.id = id
        self.title = title
        self.description = description
        # events with no date are in the 'start of the world'
        self.date = date if date is not None else datetime(1970, 1, 1)
