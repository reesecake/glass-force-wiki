from app.forms import AddCharacterForm
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user

from crud import Session
from app.models import Character
from api import app, db


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
    if not current_user.is_authenticated:
        flash('Please login or register to add entries.')
        return redirect(url_for('index'))

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
    character = db.session.query(Character).filter_by(name=pc_id).first()
    form = AddCharacterForm()

    if form.validate_on_submit():

        character.name = form.name.data
        character.desc = form.desc.data
        character.race = form.race.data
        character.char_class = form.char_class.data
        character.player_character = form.player_character.data

        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('view_character', pc_id=form.name.data))
    elif request.method == 'GET':
        form.name.data = character.name
        form.desc.data = character.desc
        form.race.data = character.race
        form.char_class.data = character.char_class
        form.player_character.data = character.player_character

    return render_template('characters/edit_character.html', form=form, character=character)


@app.route('/players/<string:pc_id>/delete', methods=('POST',))
def delete(pc_id):
    """
    Deletes the character from the database.

    :param pc_id: str - character being deleted
    """
    if not current_user.is_authenticated:
        flash('Please login or register to add entries.')
        return redirect(url_for('view_character', pc_id=pc_id))

    character = get_pc(pc_id)
    s = Session()
    s.delete(character)
    s.commit()
    flash('"{}" was successfully deleted!'.format(character.name))

    s.close()
    return redirect(url_for('get_all_characters'))
