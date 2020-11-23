from flask import ( g, redirect, url_for )
from tmc.db import get_db
from attackcti import attack_client

# Get table element by ID
def get_element_id(table, column, value): #FROM MOBILE, TECHNIQUE 'COMPROMISE' needs fixing

    value2 = value.replace('-', ' ').lower()

    db = get_db()
    try:
        query = db.execute(
            'SELECT id FROM {} WHERE lower({}) is ?'.format(table, column),
            (value2,)
            )
        result = query.fetchone()
        return result['id']
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 