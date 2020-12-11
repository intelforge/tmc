from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts

# Get list of all adversaries per event available in the database.
def get_adversaries_x_event():

    db = get_db()
    try:
        db.row_factory = make_dicts
        #db.row_factory = lambda cursor, row: {row: row[0]}
        query = db.execute(
            'select a.adversary_id, a.adversary_name, event_name, event_description from events e \
            inner join adversaries_x_events ae on ae.event_id = e.id \
            inner join adversaries a on a.id = ae.adversary_id ORDER BY adversary_name').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 