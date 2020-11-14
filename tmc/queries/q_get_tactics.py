from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all techniques available in the database.
def get_tactics():

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            'SELECT tactic_id as ID, tactic_name as Name, tactic_description as Description FROM tactics ORDER BY tactic_id').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 