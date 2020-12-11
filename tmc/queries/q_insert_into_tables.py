from flask import ( g, redirect, url_for )
from tmc.db import get_db

# Isert into db for any table
def insert_into_tables(table, element_id, element_name, element_description):

    table_id = table[:-1] + '_id'
    table_name = table[:-1] + '_name'
    table_description = table[:-1] + '_description'
    
    author_id = g.user['id']

    g.db = get_db()
    
    query='INSERT INTO {} ({}, {}, {}, {}) VALUES (?, ?, ?, ?)'.format(table, 'author_id', table_id, table_name, table_description)
    
    result = g.db.execute(query, (author_id, element_id, element_name, element_description))
    g.db.commit()
    element_id = result.lastrowid
    
    return element_id