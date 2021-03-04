from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# TODO: figure this out or remove it
# bootstrap = Bootstrap(app)

from app import routes

# # TODO: remove -------------------------------------------------------
#
# @app.route("/add")
# def add_book():
#     name = request.args.get('name')
#     author = request.args.get('author')
#     published = request.args.get('published')
#     try:
#         book = Book(
#             name=name,
#             author=author,
#             published=published
#         )
#         db.session.add(book)
#         db.session.commit()
#         return "Book added. book id={}".format(book.id)
#     except Exception as e:
#         return str(e)
#
#
# @app.route("/getall")
# def get_all():
#     try:
#         books = Book.query.all()
#         return jsonify([e.serialize() for e in books])
#     except Exception as e:
#         return str(e)
#
#
# @app.route("/get/<id_>")
# def get_by_id(id_):
#     try:
#         book = Book.query.filter_by(id=id_).first()
#         return jsonify(book.serialize())
#     except Exception as e:
#         return str(e)
#
#
# @app.route("/add/form", methods=['GET', 'POST'])
# def add_book_form():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         author = request.form.get('author')
#         published = request.form.get('published')
#         try:
#             book = Book(
#                 name=name,
#                 author=author,
#                 published=published
#             )
#             db.session.add(book)
#             db.session.commit()
#             return "Book added. book id={}".format(book.id)
#         except Exception as e:
#             return str(e)
#     return render_template("getdata.html")
#
#
# # TODO: end remove -------------------------------------------------------------
