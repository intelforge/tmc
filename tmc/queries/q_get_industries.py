from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all industries available in the database.
def get_industries():

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            'SELECT id, industry_name as Industry FROM industries ORDER BY industry_name ASC').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 