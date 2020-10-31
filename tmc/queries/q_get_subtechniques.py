from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all subtechniques available in the database.
def get_subtechniques():

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            'SELECT subtechnique_id as ID, subtechnique_name as Name, subtechnique_description as Description FROM subtechniques ORDER BY subtechnique_id').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 