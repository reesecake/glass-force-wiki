from crud import Session
from app.models import Character, Entry, User, Location
from api import app, db

@app.route('/react')
def react_index():
    return app.send_static_file('index.html')

@app.route('/api/pcs')
def api_get_all_pcs():
    """Returns a dictionary describing all PCs"""

    try:
        characters = db.session.query(Character).filter_by(player_character=True).all()

        resp = dict()
        for c in characters:
            resp[c.id] = c.serialize()
        return resp
    except Exception as e:
        return str(e)
