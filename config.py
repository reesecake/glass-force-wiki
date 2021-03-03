import os

basedir = os.path.abspath(os.path.dirname(__file__))


DATABASE_URI = os.getenv('DATABASE_URL')  # 'postgres+psycopg2://postgres:root@localhost:5432/tutorial_db'


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secret bonk key'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # APP_SETTINGS = os.environ['APP_SETTINGS']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
