from flask import ( g, redirect, url_for )
from tmc.db import get_db
from attackcti import attack_client

# Insert relation tool_x_technique
def insert_tool_x_techn(tool_id, technique_id):
    author_id = g.user['id']

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)'.format('tools_x_techniques', 'author_id', 'tool_id', 'technique_id')

    g.db.execute(query, (author_id, tool_id, technique_id))
    g.db.commit()

    return redirect(url_for('maps.completed'))
