from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all industries available in the database.
def get_countries():

    db = get_db()
    try:
        db.row_factory = lambda cursor, row: row[0]
        query = db.execute(
            'SELECT country FROM countries ORDER BY country').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 