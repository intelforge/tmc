from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts

# Get list of all events available in the database.
def get_events():

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            'SELECT event_id, event_name, event_description, event_industry FROM events').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 