from flask import ( g, redirect, url_for )
from tmc.db import get_db
from attackcti import attack_client

# Insert relation tool_x_technique
def insert_adversary_x_tool(adversary_id, tool_id):
    author_id = g.user['id']

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)'.format('adversaries_x_tools', 'author_id', 'adversary_id', 'tool_id')

    g.db.execute(query, (author_id, adversary_id, tool_id))
    g.db.commit()

    return redirect(url_for('maps.completed'))