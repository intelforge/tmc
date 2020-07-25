from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all adversaries available in the database.
def get_tools():

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            'SELECT tool_id as ID, tool_name as Name, tool_description as Description, tool_aliases as Identifiers FROM tools ORDER BY Name').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 