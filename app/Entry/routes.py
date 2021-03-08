from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user

from crud import Session
from app.models import Entry
from api import app, db


# Helper function
def get_entry(id_):
    """
    Gets the Entry corresponding to id_ from the database.

    :type id_: int
    :return: Entry
    """
    s = Session()

    session_entry = s.query(Entry).filter_by(id=id_).first()
    s.close()
    return session_entry


@app.route('/entries/<int:post_id>')
def entry(post_id):
    """
    :param post_id: int - integer of an Entry to display its contents to a page.
    """
    post = get_entry(post_id)
    return render_template('entries/entry.html', entry=post)


@app.route('/entries')
def all_entries():
    """
    Gets a list of all Entries and displays their title and creation time in the template.
    """
    s = Session()

    try:
        entries_list = s.query(Entry).all()
        s.close()
        return render_template("entries/entries_list.html", entries=entries_list)
    except Exception as e:
        return str(e)


@app.route('/entries/add', methods=('GET', 'POST'))
def add_entry():
    """
    Presents a form to add a new entry to the database.
    Requires the user to be logged in.
    """
    if not current_user.is_authenticated:
        flash('Please login or register to add entries.')
        return redirect(url_for('index'))

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
                    content=content,
                    user_id=current_user.get_id()
                )
                s.add(new_entry)
                s.commit()
                s.close()
                return redirect(url_for('index'))
            except Exception as e:
                s.close()
                return render_template('404_page.html', message=str(e))

    s.close()
    return render_template('entries/add_entry_form.html')
