from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all adversaries available in the database.
def get_adversaries_x_campaign():

    db = get_db()
    try:
        db.row_factory = make_dicts
        #db.row_factory = lambda cursor, row: {row: row[0]}
        query = db.execute(
            'SELECT adversary_id as ID, adversary_name as Name, adversary_identifiers as Identifiers, adversary_description as Description FROM adversaries ORDER BY Name').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 