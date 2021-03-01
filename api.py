import os

from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate

from models import db, Book, Character


def get_pc(pc_id):
    post = db.Query.get(pc_id)
    return post


app = Flask(__name__)

app.config['APP_SETTINGS'] = os.getenv('APP_SETTINGS')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    posts = []
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/players/<string:pc_id>')
def player_character(pc_id):
    pc_page = get_pc(pc_id)
    return render_template('post.html', post=pc_page)


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
        name=request.form.get('name')
        author=request.form.get('author')
        published=request.form.get('published')
        try:
            book=Book(
                name=name,
                author=author,
                published=published
            )
            db.session.add(book)
            db.session.commit()
            return "Book added. book id={}".format(book.id)
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")


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

"""
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)
"""

"""
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
"""
