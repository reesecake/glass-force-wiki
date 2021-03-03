from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Entry, Base
from config import DATABASE_URI

# Create, Read, Update, Delete
# https://github.com/LearnDataSci/articles/blob/master/Guide%20to%20Using%20Databases%20with%20Python%20Postgres%2C%20SQLAlchemy%2C%20and%20Alembic/project/crud.py

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def recreate_database():
    """
    Deletes all the tables
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    recreate_database()
    # add_data()

    entry = Entry(
            date='01/01',
            content='wow things happened here'
    )
    with session_scope() as s:
        s.add(entry)
