import os

from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm, AddCharacterForm, AddLocationForm
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_migrate import Migrate

from crud import engine, recreate_database, Session
from app.models import Character, Entry, User, Location
from api import app


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


@app.route('/')
@app.route('/index')
def index():
    s = Session()

    try:
        pcs = s.query(Character).filter_by(player_character=True).all()
        locs = s.query(Location).limit(2).all()
        s.close()
        return render_template('index.html', pcs=pcs, locations=locs)
    except Exception as e:
        return str(e)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    s = Session()
    form = LoginForm()

    if form.validate_on_submit():
        user = s.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            s.close()
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        s.close()
        return redirect(url_for('index'))

    s.close()
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        s = Session()

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        s.add(user)
        s.commit()
        s.close()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('registration.html', form=form)


@app.route('/players/<string:pc_id>')
def view_character(pc_id):
    s = Session()

    try:
        character = get_pc(pc_id)
        if character is None:
            raise Exception("Sorry, that character could not be located.")
    except Exception as e:
        s.close()
        return render_template('404_page.html', message=str(e))

    s.close()
    return render_template('characters/view_character.html', character=character)


@app.route('/players/add', methods=['GET', 'POST'])
def add_character():
    form = AddCharacterForm()

    if form.validate_on_submit():
        s = Session()

        character = Character(
            name=form.name.data,
            desc=form.desc.data,
            race=form.race.data,
            player_character=form.player_character.data
        )
        s.add(character)
        s.commit()
        s.close()
        flash('"{}" has been added as a character!'.format(form.name.data))
        return redirect(url_for('view_character', pc_id=form.name.data))

    return render_template('characters/add_char_form.html', form=form)


@app.route('/characters')
def get_all_characters():
    s = Session()

    try:
        characters = s.query(Character).all()
        s.close()
        return render_template("characters/character_list.html", characters=characters)
    except Exception as e:
        return str(e)


# TODO: fix
@app.route('/players/<string:pc_id>/edit', methods=('GET', 'POST'))
def edit_character(pc_id):
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

    return render_template('characters/edit.html', character=character)


@app.route('/players/<string:pc_id>/delete', methods=('POST',))
def delete(pc_id):
    character = get_pc(pc_id)
    s = Session()
    s.delete(character)
    s.commit()
    flash('"{}" was successfully deleted!'.format(character.name))

    s.close()
    return redirect(url_for('get_all_characters'))


@app.route('/locations/<string:loc_name>')
def location(loc_name):
    s = Session()

    loc = s.query(Location).filter_by(name=loc_name).first()
    s.close()
    return render_template('locations/location.html', location=loc)


@app.route('/locations')
def all_locations():
    s = Session()

    try:
        locations_list = s.query(Location).all()
        s.close()
        return render_template("locations/locations_list.html", locations=locations_list)
    except Exception as e:
        return str(e)


@app.route('/locations/add', methods=('GET', 'POST'))
def add_location():
    """
    Create a new location
    """
    if not current_user.is_authenticated:
        flash('Please login or register to add locations.')
        return redirect(url_for('index'))

    form = AddLocationForm()

    if form.validate_on_submit():
        s = Session()

        new_loc = Location(
            name=form.name.data,
            content=form.content.data,
            user_id=current_user.get_id()
        )
        s.add(new_loc)
        s.commit()
        # get the full data of the new loc
        loc = s.query(Location).filter_by(name=form.name.data).first()
        s.close()
        flash('"{}" has been added as a location!'.format(form.name.data))
        return redirect(url_for('location', loc_name=loc.name))

    return render_template('locations/add_location_form.html', form=form)


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
    return render_template('entries/entry.html', entry=post)


@app.route('/entries')
def all_entries():
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
    Create a new session entry
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
