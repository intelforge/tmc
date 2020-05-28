from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from tmc.auth import login_required
from tmc.db import get_db
from attackcti import attack_client
from IPython import embed

bp = Blueprint('maps', __name__)

# Homepage
@bp.route('/')
def index():

    return render_template('maps/index.html')

# Successful DB update
@bp.route('/first-time')
def first_time():
    
    print('Inserting tactics...')
    #get_tactics()
    
    print('Inserting techniques...')
    #get_techniques()
    
    print('Inserting groups...')
    #get_groups()
    
    print('Inserting tools...')
    #get_tools()
    
    print('Inserting tactics per techniques...')
    get_tacxtec()
    
    print('Inserting tools per techniques...')
    tool_x_technique()

    print('Inserting adversary per tools...')
    adversary_x_tool()

    return render_template('maps/completed.html')

# Successful DB update
@bp.route('/completed')
def completed():

    return render_template('maps/completed.html')


# ATT&CK FRAMEWORK INTERACTION 

# Adding ATT&CK Tactics
@bp.route('/attackcti_tactics', methods=('GET', 'POST'))
@login_required
def get_tactics():
    lift = attack_client()
    tactics = lift.get_tactics()

    for element in tactics:
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
    techniques = lift.get_techniques()
    error = [] 

    for element in techniques:
        technique_id = element['external_references'][0]['external_id']
        technique_name = element['name']

        try:
            technique_description = element['description']
        except KeyError:
            technique_description = ''

        try:
            technique_tactic = element['kill_chain_phases'][0]['phase_name'] 
            insert_into_table = insert('techniques', technique_id, technique_name, technique_description)
            print('Created technique %s' % technique_name)
        except KeyError:
            error.append(technique_id)
            # MOBILE TECHNIQUES MISSING TACTIC REFERENCE:
            #T1443, T1425, T1442, T1419, T1440, T1462, T1460, T1459, T1457, T1445, T1431, T1434, T1473, T1454, T1455, T1441

    print(error)

    return redirect(url_for('maps.completed'))


# Adding ATT&CK TacticxTechniques
@bp.route('/attackcti_tacxtec', methods=('GET', 'POST'))
@login_required
def get_tacxtec():
    lift = attack_client()
    techniques = lift.get_techniques()

    for element in techniques:
        technique_name = element['name']
        technique_attack_id = element['external_references'][0]['external_id']
        technique_id = get_element_id('techniques', 'technique_id', technique_attack_id)

        technique_tactic = element['kill_chain_phases'][0]['phase_name']
        tactic_id = get_element_id('tactics', 'tactic_name', technique_tactic)

        tactic_x_technique = insert_tactic_x_technique(tactic_id, technique_id)

        print('Created tactic relationship')

    return redirect(url_for('maps.completed'))


# Adding ATT&CK Adversaries
@bp.route('/attackcti_groups', methods=('GET', 'POST'))
@login_required
def get_groups():
    lift = attack_client()
    groups = lift.get_groups()

    for element in groups:
        group_id = element['external_references'][0]['external_id']
        group_name = element['name']

        try:
            group_description = element['description']
        except KeyError:
            group_description = ''
        try:
            group_aliases = element['aliases']
        except KeyError:
            group_aliases = ''

        insert_into_table = insert('adversaries', group_id, group_name, group_description)

    return redirect(url_for('maps.completed'))


# Adding ATT&CK Tools
@bp.route('/attackcti_tools', methods=('GET', 'POST'))
@login_required
def get_tools():
    lift = attack_client()
    tools = lift.get_software()

    for element in tools:
        tool_id = element['external_references'][0]['external_id']
        tool_name = element['name']
        try:
            tool_description = element['description']
        except KeyError:
            tool_description = ''
        try:
            tool_aliases = element['x_mitre_aliases']
        except KeyError:
            tool_aliases = ''

        insert_into_table = insert('tools', tool_id, tool_name, tool_description)

    return redirect(url_for('maps.completed'))


# INTERACTION WITH DATABASE

# Get table element by ID // merge two in one
def get_element_id(table, column, value): #FROM MOBILE, TECHNIQUE 'COMPROMISE' needs fixing

    value2 = value.replace('-', ' ')

    db = get_db()
    try:
        query = get_db().execute(
            'SELECT id FROM {} WHERE lower({}) = ?'.format(table, column),
            (value2.lower(),)
            ).fetchone()
        result = query[0]
        return result
    except TypeError:
        embed()



# Isert into db from any table
def insert(table, element_id, element_name, element_description):

    if table == 'adversaries':
        table_id = 'adversary_id'
        table_name = 'adversary_name'
        table_description = 'adversary_description'
    else:
        table_id = table[:-1] + '_id'
        table_name = table[:-1] + '_name'
        table_description = table[:-1] + '_description'
    
    author_id = g.user['id']

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}, {}) VALUES (?, ?, ?, ?)'.format(table, 'author_id', table_id, table_name, table_description)
    g.db.execute(query, (author_id, element_id, element_name, element_description))
    g.db.commit()
    return redirect(url_for('maps.completed'))


# DB INTERACTION FROM FRONT-END

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


# Creates the new tool in the database
@bp.route('/create-tool', methods=('GET', 'POST'))
@login_required
def create_tool():
    if request.method == 'POST':
        tool_name = request.form['name']
        tool_description = request.form['description']
        error = None

        if not tool_name:
            error = 'Tool name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tools (tool_name, tool_description, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('maps.create_tool'))

    return render_template('maps/create-tool.html')


# Insert Tools x Techniques
@bp.route('/attackcti_toolxtech', methods=('GET', 'POST'))
@login_required
def tool_x_technique():
    lift = attack_client()
    tools = lift.get_software()
    
    for element in tools:
        tool_attack_id = element['external_references'][0]['external_id']
        tool_id = get_tools_by_attack_id(tool_attack_id)
        techniques_used = lift.get_techniques_used_by_software(element)

        for technique in techniques_used:
            technique_attack_id = technique['external_references'][0]['external_id']
            technique_id = get_element_id('techniques', 'technique_id', technique_attack_id)
            
            result = insert_tool_x_techn(tool_id, technique_id)

    return True


# Insert relation adversary_x_tool
@bp.route('/attackcti_advxtool', methods=('GET', 'POST'))
@login_required
def adversary_x_tool():
    lift = attack_client()
    groups = lift.get_groups()
    
    for element in groups:
        adversary_attack_id = element['external_references'][0]['external_id']
        adversary_id = get_adversary_by_attack_id(adversary_attack_id)
        adversary = element['name']

        tools_used = lift.get_software_used_by_group(element)

        for tool in tools_used:
            tool_attack_id = tool['external_references'][0]['external_id']
            tool_id = get_element_id('tools', 'tool_id', tool_attack_id)

            result = insert_adversary_x_tool(adversary_id, tool_id)
        
    return True


# Insert relation tool_x_technique
def insert_tool_x_techn(tool_id, technique_id):
    author_id = g.user['id']

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)'.format('tools_x_techniques', 'author_id', 'tool_id', 'technique_id')

    g.db.execute(query, (author_id, tool_id, technique_id))
    g.db.commit()

    return redirect(url_for('maps.completed'))


# Insert relation tool_x_technique
def insert_adversary_x_tool(adversary_id, tool_id):
    author_id = g.user['id']

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)'.format('adversaries_x_tools', 'author_id', 'adversary_id', 'tool_id')

    g.db.execute(query, (author_id, adversary_id, tool_id))
    g.db.commit()

    return redirect(url_for('maps.completed'))


# Insert relation tactic_x_technique
def insert_tactic_x_technique(tactic_id, technique_id):
    author_id = g.user['id']

    g.db = get_db()
    query='INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)'.format('tactics_x_techniques', 'author_id', 'tactic_id', 'technique_id')

    g.db.execute(query, (author_id, tactic_id, technique_id))
    g.db.commit()

    return redirect(url_for('maps.completed'))
