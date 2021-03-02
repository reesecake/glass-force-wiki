import os

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_migrate import Migrate

from crud import engine, recreate_database, Session
from models import db, Character, Entry


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

app.config['APP_SETTINGS'] = os.getenv('APP_SETTINGS')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret bonk key'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    s = Session()
    s.close_all()
    posts = []
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/players/<string:pc_id>')
def player_character(pc_id):
    s = Session()

    try:
        character = s.query(Character).filter_by(name=pc_id).first()
        if character is None:
            raise Exception("Sorry, that character could not be located.")
    except Exception as e:
        s.close()
        return render_template('404_page.html', message=str(e))

    s.close()
    return render_template('player_character.html', character=character)


@app.route('/players/add', methods=['GET', 'POST'])
def add_character():
    s = Session()

    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        race = request.form.get('race')
        try:
            character = Character(
                name=name,
                desc=desc,
                race=race
            )
            s.add(character)
            s.commit()
            s.close()
            return redirect(url_for('player_character', pc_id=name))
        except Exception as e:
            return str(e)
    return render_template("char_form.html")


@app.route('/characters')
def get_all_characters():
    s = Session()

    try:
        characters = s.query(Character).all()
        s.close()
        return render_template("character_list.html", characters=characters)
    except Exception as e:
        return str(e)


@app.route('/players/<string:pc_id>/edit', methods=('GET', 'POST'))
def edit(pc_id):
    character = get_pc(pc_id)

    s = Session()

    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']

        if not name:
            flash('name is required!')
        else:
            s.execute('UPDATE character SET name = ?, desc = ? WHERE name = ?',
                      (name, desc, name))
            s.commit()
            s.close()
            return redirect(url_for('index'))

    return render_template('edit.html', character=character)


@app.route('/players/<string:pc_id>//delete', methods=('POST',))
def delete(pc_id):
    character = get_pc(pc_id)
    s = Session()
    s.delete(character)
    s.commit()
    flash('"{}" was successfully deleted!'.format(character.name))

    s.close()
    return redirect(url_for('get_all_characters'))


@app.route("/bonk")
def bonk():
    return render_template("bonk.html")


@app.route('/db/reset', methods=['GET', 'POST'])
def db_reset():
    s = Session()

    if request.method == 'POST':
        password = request.form['password']

        try:
            if password == 'bonk':
                recreate_database()
                flash('Database tables were reset')
        except Exception as e:
            return str(e)
    return render_template("db_reset.html")


if __name__ == '__main__':
    app.run()


@app.route('/entries/<int:post_id>')
def entry(post_id):
    post = get_entry(post_id)
    return render_template('entry.html', entry=post)


@app.route('/entries')
def all_entries():
    s = Session()

    try:
        entries_list = s.query(Entry).all()
        s.close()
        return render_template("entries_list.html", entries=entries_list)
    except Exception as e:
        return str(e)


@app.route('/entries/create', methods=('GET', 'POST'))
def create():
    s = Session()

    if request.method == 'POST':
        date = request.form['date']
        content = request.form['content']

        if not date:
            flash('Date is required!')
        else:
            try:
                new_entry = Entry(
                    date=date,
                    content=content
                )
                s.add(new_entry)
                s.commit()
                s.close()
                return redirect(url_for('index'))
            except Exception as e:
                s.close()
                return render_template('404_page.html', message=str(e))

    s.close()
    return render_template('create.html')


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
