from datetime import datetime
from hashlib import md5

from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from api import login, db


Base = declarative_base()
"""
If Base is passed into the class definition, Alembic will not migrate the table.
ex. User(Base) will get users dropped if it was originally User(db.Model)
"""


@login.user_loader
def load_user(id_):
    return db.session.query(User).get(int(id_))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Entry', backref='author', lazy='dynamic')
    location_posts = db.relationship('Location', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': 'private!',
            'about_me': self.about_me,
            'last_seen': self.last_seen
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True)
    desc = db.Column(db.String())
    race = db.Column(db.String())
    player_character = db.Column(db.Boolean())
    char_class = db.Column(db.String())

    def __init__(self, name, desc, race, char_class, player_character):
        self.name = name
        self.desc = desc
        self.race = race
        self.char_class = char_class
        self.player_character = player_character

    def __repr__(self):
        return '<name {}>'.format(self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'race': self.race,
            'char_class': self.char_class,
            'player_character': self.player_character
        }


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, content, user_id):
        self.name = name,
        self.content = content,
        self.user_id = user_id

    def __repr__(self):
        return '<Location {}>'.format(self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'timestamp': self.timestamp,
            'content': self.content,
            'user_id': self.user_id
        }


class Entry(db.Model):
    """
    Class for dnd session data
    """
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String())  # could be datetime
    content = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, date, content, user_id):
        self.date = date
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return '<entry id: {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'content': self.content,
            'timestamp': self.timestamp,
            'user_id': self.user_id
        }
