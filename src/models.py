"""
    Models contains the python representations for our database tables and 
    contains various utility methods for serializing the data for transfer
"""

from sqlalchemy import Column, Integer, String, Float, Date
from database import Base
from json import dumps

class Device(Base):
    """ Represents a robomussell temperature entry """

    __tablename__ = "devs"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    date = Column(Date)
    reading = Column(Float)

    def __init__(self, name, date, reading):
        self.name = name
        self.date = date
        self.reading = reading
   
    def to_json(self):
        return {"name": self.name, 
                "date": self.date.strftime("%Y/%m/%d %H:%M"),
                "reading": self.reading}

    def __repr__(self):
        return "<Device %s %s %f>" % (self.name, self.date, self.reading)
