from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    published = db.Column(db.String())

    def __init__(self, name, author, published):
        self.name = name
        self.author = author
        self.published = published

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'published': self.published
        }


class Character(db.Model):
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
