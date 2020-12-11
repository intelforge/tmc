from flask import ( g, redirect, url_for )
from tmc.db import get_db

# Isert into db for any table
def insert_into_events(event_name, event_description, event_url):
    
    author_id = g.user['id']

    g.db = get_db()
    
    query='INSERT INTO events ({}, {}, {}, {}) VALUES (?, ?, ?, ?)'.format('author_id', 'event_name', 'event_description', 'event_url')
    
    result = g.db.execute(query, (author_id, event_name, event_description, event_url))
    g.db.commit()
    element_id = result.lastrowid
    
    return element_id