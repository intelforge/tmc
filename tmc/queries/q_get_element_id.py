from flask import ( g, redirect, url_for )
from tmc.db import get_db
from attackcti import attack_client

# Get table element by ID // merge two in one
def get_element_id(table, column, value): #FROM MOBILE, TECHNIQUE 'COMPROMISE' needs fixing

    value2 = value.replace('-', ' ')

    db = get_db()
    try:
        query = get_db().execute(
            'SELECT id FROM {} WHERE lower({}) = ?'.format(table, column),
            (value2.lower(),)
            ).fetchone()
        result = query[0]
        return result
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 