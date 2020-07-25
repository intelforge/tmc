from flask import ( g, redirect, url_for )
from tmc.db import get_db
from attackcti import attack_client
from IPython import embed

# Get list of all adversaries available in the database.
def get_adversaries_names():

    db = get_db()
    try:
        db.row_factory = lambda cursor, row: row[0]
        query = db.execute(
            'SELECT adversary_name FROM adversaries ORDER BY adversary_name').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 