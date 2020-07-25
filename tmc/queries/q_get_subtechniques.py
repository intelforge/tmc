from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all adversaries available in the database.
def get_subtechniques():

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            'SELECT subtechnique_id, subtechnique_name, subtechnique_description FROM adversaries').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 