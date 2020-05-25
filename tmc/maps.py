from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from tmc.auth import login_required
from tmc.db import get_db
from attackcti import attack_client
from IPython import embed

bp = Blueprint('maps', __name__)

#NOT IN USE, SEARCH FOR HOME - the Select here is not useful
@bp.route('/')
def index():

    return render_template('maps/index.html')


@bp.route('/completed')
def completed():

    return render_template('maps/completed.html')


# Creates the new adversary in the database
@bp.route('/create-adversary', methods=('GET', 'POST'))
@login_required
def create_adversary():
    if request.method == 'POST':
        adversary_name = request.form['name']
        adversary_description = request.form['description']
        error = None

        if not adversary_name:
            error = 'Adversary name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO adversaries (adversary_name, adversary_description, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('maps.create_adversary'))

    return render_template('maps/create-adversary.html')


# Creates the new technique in the database
@bp.route('/create-technique', methods=('GET', 'POST'))
@login_required
def create_technique():
    if request.method == 'POST':
        tool_name = request.form['name']
        tool_description = request.form['description']
        error = None

        if not tool_name:
            error = 'Technique name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO techniques (technique_name, technique_description, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('maps.create_technique'))

    return render_template('maps/create-technique.html')


# Adding ATT&CK Tactics
@bp.route('/attackcti_tactics', methods=('GET', 'POST'))
@login_required
def get_tactics():
    lift = attack_client()
    enterprise_tactics = lift.get_enterprise_tactics()

    for element in enterprise_tactics:
        tactic_id = element['external_references'][0]['external_id']
        tactic_name = element['name']
        tactic_description = element['description']

        insert_into_table = insert('tactics', tactic_id, tactic_name, tactic_description)
        print('Created tactic %s' % tactic_name)

    return redirect(url_for('maps.completed'))



# Adding ATT&CK Techniques
@bp.route('/attackcti_techniques', methods=('GET', 'POST'))
@login_required
def get_techniques():
    lift = attack_client()
    enterprise_techniques = lift.get_enterprise_techniques()

    for element in enterprise_techniques:
        technique_id = element['external_references'][0]['external_id']
        technique_name = element['name']
        technique_description = element['description']
        technique_tactic = element['kill_chain_phases'][0]['phase_name'] 

        insert_into_table = insert('techniques', technique_id, technique_name, technique_description)

        print('Created technique %s' % technique_name)

        tactic_x_technique = insert_tactic_x_technique(technique_tactic, technique_name)

        print('Created tactic relationship')

    return redirect(url_for('maps.completed'))


# Get last item ID
def get_last_item_id(table):
    db = get_db()
    query = 'SELECT * FROM {} ORDER BY id DESC LIMIT 1'.format(table)
    db.execute(query)
    result = db.commit()
    if result:
        new_id = result + 1
    else:
        new_id = 1

    return new_id


# Isert into db from any table
def insert(table, element_id, element_name, element_description):
    id = get_last_item_id(table)
    table_id = table[:-1] + '_id'
    table_name = table[:-1] + '_name'
    table_description = table[:-1] + '_description'
    author_id = g.user['id']

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}, {}) VALUES (?, ?, ?, ?)'.format(table, 'author_id', table_id, table_name, table_description)
    g.db.execute(query, (author_id, element_id, element_name, element_description))
    g.db.commit()
    return redirect(url_for('maps.index'))


# Insert relation tactic_x_technique
def insert_tactic_x_technique(technique_tactic, technique_name):
    author_id = g.user['id']

    tactic_id = get_element_id('tactics', 'tactic_name', technique_tactic)
    technique_id = get_element_id('techniques', 'technique_name', technique_name)

    db = get_db()
    db.execute(
        'INSERT INTO tactics_x_techniques (author_id, tactic_id, technique_id) VALUES (?, ?, ?)',
        (author_id, tactic_id, technique_id)
    )
    result = db.commit()

    return result


# Get table element by ID
def get_element_id(table, column, value):

    db = get_db()
    query = 'SELECT id FROM {} WHERE ? like ?'.format(table)
    db.execute(query, (column, value, ))
    result = db.commit()

    return result
