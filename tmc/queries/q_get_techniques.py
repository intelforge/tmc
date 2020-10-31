from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all techniques available in the database.
def get_techniques():

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            'SELECT technique_id as ID, technique_name as Name, technique_description as Description FROM techniques ORDER BY technique_id').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 