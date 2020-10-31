from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all industries available in the database by name.
def get_industries_names():

    db = get_db()
    try:
        db.row_factory = lambda cursor, row: row[0]
        query = db.execute(
            'SELECT industry_name as Industry FROM industries ORDER BY industry_name ASC').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 