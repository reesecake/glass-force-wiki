from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

Base = declarative_base()


class Character(Base):
    __tablename__ = 'characters'

    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), primary_key=True)
    desc = db.Column(db.String())
    race = db.Column(db.String())

    def __init__(self, name, desc, race):
        self.name = name
        self.desc = desc
        self.race = race

    def __repr__(self):
        return '<id {}>'.format(self.name)

    def serialize(self):
        return {
            'name': self.name,
            'author': self.desc,
            'published': self.race
        }


class Entry(Base):
    """
    Class for dnd session data
    """
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String())  # could be datetime
    content = db.Column(db.String())

    def __init__(self, date, content):
        # self.id = id
        self.date = date
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'content': self.content
        }
