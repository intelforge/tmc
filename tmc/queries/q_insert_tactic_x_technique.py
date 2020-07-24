from flask import ( g, redirect, url_for )
from tmc.db import get_db
from attackcti import attack_client

# Insert relation tactic_x_technique
def insert_tactic_x_technique(tactic_id, technique_id):
    author_id = g.user['id']

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)'.format('tactics_x_techniques', 'author_id', 'tactic_id', 'technique_id')

    g.db.execute(query, (author_id, tactic_id, technique_id))
    g.db.commit()

    return redirect(url_for('maps.completed'))
