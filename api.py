from config import Config
from flask import Flask
from flask_migrate import Migrate

from crud import Session
from app.models import db, Character, Entry


def get_pc(pc_id):
    s = Session()

    character = s.query(Character).filter_by(name=pc_id).first()
    s.close()
    return character


def get_entry(id_):
    s = Session()

    session_entry = s.query(Entry).filter_by(id=id_).first()
    s.close()
    return session_entry


app = Flask(__name__)
app.config.from_object(Config)

# app.config['APP_SETTINGS'] = os.getenv('APP_SETTINGS')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'secret bonk key'
db.init_app(app)
migrate = Migrate(app, db)

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
