from app.forms import AddLocationForm
from flask import render_template, redirect, url_for, flash
from flask_login import current_user

from crud import Session
from app.models import Location
from api import app, db


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
