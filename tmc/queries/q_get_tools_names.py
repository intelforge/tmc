from flask import ( g, redirect, url_for )
from tmc.db import get_db
from attackcti import attack_client
from IPython import embed

# Get list of all adversaries available in the database by name.
def get_tools_names():

    db = get_db()
    try:
        db.row_factory = lambda cursor, row: row[0]
        query = db.execute(
            'SELECT tool_name FROM tools ORDER BY tool_name').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 