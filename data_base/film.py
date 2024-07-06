import datetime

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String, default="active")  # Add status column with a default value
    date_in = Column(Date, default=datetime.date.today())
    date_out = Column(Date)
    comment = Column(String)

    def __init__(self, title, comment=None):
        self.title = title
        self.comment = comment
        self.date_in = datetime.date.today()
        self.date_out = None

    def status_change(self):
        if self.status == "active":
            self.status = "watched"
            self.date_out = datetime.date.today()
        else:
            return False
