import os
from datetime import datetime

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm, AddCharacterForm, AddLocationForm, EditProfileForm
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_migrate import Migrate

from crud import engine, recreate_database, Session
from app.models import Character, Entry, User, Location
from api import app


def get_pc(pc_id):
    """
    Gets the Character corresponding to pc_id from the database.

    :type pc_id: str
    :return: Character
    """
    s = Session()

    character = s.query(Character).filter_by(name=pc_id).first()
    s.close()
    return character


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


@app.route('/')
@app.route('/index')
def index():
    """
    Passes a list of player-character Characters and two locations to the template.
    """
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
    """
    Gives an anonymous user the login form and checks their credentials against users in the database.
    """
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
    """
    Logs the current_user out and redirects them to index.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Presents an anonymous user with the registration form and adds their info to the database.
    Uses user.set_password() to hash their password (instead of storing it plaintext).
    """
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


@app.route('/user/<username>')
@login_required
def user(username):
    """
    Gets the User data from the database given a username and renders the profile page.

    :param username: the user's username
    :type username: str
    """
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]

    return render_template('user_profile.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Gives the user a form to edit their profile and updates the information in the database.
    """
    form = EditProfileForm()

    if form.validate_on_submit():
        s = Session()

        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        s.commit()
        s.close()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', form=form)


@app.before_request
def before_request():
    """
    Updates the current user's last_seen field.
    """
    if current_user.is_authenticated:
        s = Session()
        current_user.last_seen = datetime.utcnow()
        s.commit()
        s.close()


@app.route('/players/<string:pc_id>')
def view_character(pc_id):
    """
    Displays the information page about a character.
    Note: pc_id is the name of the character and not id.

    :param pc_id: string - the name of the character to view
    """
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
    """
    Presents a form to create a character that is added to the database.
    Flashes success and redirects to the page of that character.
    """
    form = AddCharacterForm()

    if form.validate_on_submit():
        s = Session()

        if form.char_class.data == 'Select a Class':
            form.char_class.data = None
        if form.race.data == 'Select a Race':
            form.race.data = None

        character = Character(
            name=form.name.data,
            desc=form.desc.data,
            race=form.race.data,
            char_class=form.char_class.data,
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
    """
    Gets a list of all characters in the database and the template displays their name and race.
    """
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
    """
    Presents a form to edit an existing character corresponding to pc_id.
    Note: pc_id is the string name of the character and not the actual id.

    :param pc_id: str - character's name
    """
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
    """
    Deletes the character from the database.

    :param pc_id: str - character being deleted
    """
    character = get_pc(pc_id)
    s = Session()
    s.delete(character)
    s.commit()
    flash('"{}" was successfully deleted!'.format(character.name))

    s.close()
    return redirect(url_for('get_all_characters'))


@app.route('/locations/<string:loc_name>')
def location(loc_name):
    """
    Displays the page about the given location.

    :param loc_name: str - name of the location
    """
    s = Session()

    loc = s.query(Location).filter_by(name=loc_name).first()
    s.close()
    return render_template('locations/location.html', location=loc)


@app.route('/locations')
def all_locations():
    """
    Gets a list of all locations from the database and passes it to the template.
    The template iterates through the list and displays some info on the location.
    """
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
    Adds a new location to the database from the given form.
    Only reachable if the user is logged in.
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
    """
    Placeholder template/route
    """
    return render_template("bonk.html")


@app.route('/db/reset', methods=['GET', 'POST'])
def db_reset():
    """
    Gives a form requiring an un-hashed, plaintext password to drop and recreate all the tables in the database.
    """
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
