from flask import ( g, redirect, url_for )
from tmc.db import get_db

# Insert relation adversary per tool
def insert_event_x_industry(event_id, industry_id):
    author_id = g.user['id']

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)'.format('events_x_industries', 'author_id', 'event_id', 'industry_id')

    result = g.db.execute(query, (author_id, event_id, industry_id))
    g.db.commit()
    element_id = result.lastrowid

    return element_id