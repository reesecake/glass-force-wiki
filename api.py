import os

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_migrate import Migrate

from crud import engine, recreate_database, Session
from models import db, Book, Character, Base


def get_pc(pc_id):
    s = Session()

    character = s.query(Character).filter_by(name=pc_id).first()
    s.close()
    return character


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
    except Exception as e:
        return str(e)

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


# TODO: remove -------------------------------------------------------

@app.route("/add")
def add_book():
    name = request.args.get('name')
    author = request.args.get('author')
    published = request.args.get('published')
    try:
        book = Book(
            name=name,
            author=author,
            published=published
        )
        db.session.add(book)
        db.session.commit()
        return "Book added. book id={}".format(book.id)
    except Exception as e:
        return str(e)


@app.route("/getall")
def get_all():
    try:
        books = Book.query.all()
        return jsonify([e.serialize() for e in books])
    except Exception as e:
        return str(e)


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book = Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return str(e)


@app.route("/add/form", methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        name = request.form.get('name')
        author = request.form.get('author')
        published = request.form.get('published')
        try:
            book = Book(
                name=name,
                author=author,
                published=published
            )
            db.session.add(book)
            db.session.commit()
            return "Book added. book id={}".format(book.id)
        except Exception as e:
            return str(e)
    return render_template("getdata.html")


# TODO: end remove -------------------------------------------------------------


@app.route("/bonk")
def bonk():
    return render_template("bonk.html")


if __name__ == '__main__':
    app.run()

"""
@app.route('/<int:post_id>')
def post(post_id):
    post_num = get_post(post_id)
    return render_template('post.html', post=post_num)
"""


@app.route('/create', methods=('GET', 'POST'))
def create():
    # if request.method == 'POST':
    #     title = request.form['title']
    #     content = request.form['content']
    #
    #     if not title:
    #         flash('Title is required!')
    #     else:
    #         conn = get_db_connection()
    #         conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
    #                      (title, content))
    #         conn.commit()
    #         conn.close()
    #         return redirect(url_for('index'))

    return render_template('create.html')
