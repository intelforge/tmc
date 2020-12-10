from flask import ( g, redirect, url_for )
from tmc.db import get_db

# Insert relation tool_x_technique
def insert_tool_x_techn(table, tool_id, technique_id):
    try:
    	author_id = g.user['id']
    except (NameError, TypeError) as error:
    	author_id = 1

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)'.format(table, 'author_id', 'tool_id', 'technique_id')

    result = g.db.execute(query, (author_id, tool_id, technique_id))
    g.db.commit()
    element_id = result.lastrowid

    return element_id
