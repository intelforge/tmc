from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all techniques available in the database.
def get_techniques(technique=''):

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            'SELECT technique_id as ID, technique_name as Name, technique_description as Description FROM techniques ')

        if not technique:
            query = query + ' ORDER BY adversary_name ASC'
            executed_query = db.execute(query).fetchall()
            return executed_query
        else:
            query = db.execute( query + ' WHERE lower(technique_name) is ? ORDER BY technique_name ASC', (technique,))
            result = query.fetchone()
        return result
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 