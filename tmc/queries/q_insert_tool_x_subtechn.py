from flask import ( g, redirect, url_for )
from tmc.db import get_db

# Insert relation tool_x_subtechnique
def insert_tool_x_subtechn(table, tool_id, subtechnique_id):
    author_id = g.user['id']

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)'.format(table, 'author_id', 'tool_id', 'subtechnique_id')

    result = g.db.execute(query, (author_id, tool_id, subtechnique_id))
    g.db.commit()
    element_id = result.lastrowid

    return element_id
