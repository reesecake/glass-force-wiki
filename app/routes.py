import os
from datetime import datetime

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm, AddCharacterForm, AddLocationForm, EditProfileForm
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_migrate import Migrate

from crud import engine, recreate_database, Session
from app.models import Character, Entry, User, Location
from api import app, db


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
    user = db.session.query(User).filter_by(username=username).first_or_404()

    posts = db.session.query(User).join(Entry, Entry.user_id == user.id).all()

    return render_template('user_profile.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Gives the user a form to edit their profile and updates the information in the database.
    """
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data

        db.session.commit()
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
