from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


app = Flask(__name__, static_folder='react-front/build', static_url_path='/')
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# TODO: figure this out or remove it
bootstrap = Bootstrap(app)

from app import routes
from app.Character import routes
from app.Entry import routes
from app.Location import routes
from app.Api import routes
