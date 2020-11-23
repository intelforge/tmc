from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_paginate import Pagination, get_page_args
from werkzeug.exceptions import abort

from tmc.auth import login_required
from tmc.db import get_db
from attackcti import attack_client
from IPython import embed
import tmc.queries as q
from tmc.queries import *
import tmc.processor as processor
import json

bp = Blueprint('maps', __name__, template_folder='templates')

# Homepage
@bp.route('/', methods=["GET", "POST"])
def index():

    adversaries_list = q.q_get_adversaries.get_adversaries()
    tools_list = q.q_get_tools.get_tools()
    industries_list = q.q_get_industries.get_industries()

    return render_template('maps/index.html', adversaries_list=adversaries_list, tools_list=tools_list, industries_list=industries_list)

@bp.route('/tram-interaction', methods=["GET", "POST"])
def tram_mapping():

    if request.method == "POST":

        req = request.form
        adversary = req['adversary']
        tool = req['tool']
        event_name = req['event_name']
        event_description = req['event_description']
        industry = req['industry']
        url = req['event_description']

    event = insert_new_event()
    adv_x_event=insert_adversary_x_event(adversary, event)
    get_techniques = sent_url_to_tram()
    tool_x_techniques = insert_tool_x_techniques()

    return render_template('maps/index.html')

def insert_new_event():

    return True


def insert_adversary_x_event(adversary, event):

    return True


def sent_url_to_tram():

    return True


def insert_tool_x_techniques():

    return True

# List all posible actions to display data
@bp.route('/explore')
def explore():

    return render_template('maps/explore.html') 

# Displays all adversaries in the DB
@bp.route('/explore-adversaries')
def explore_adversaries():

    title='Adversaries'
    adversaries = q.q_get_adversaries.get_adversaries()
    adversaries_th = adversaries[0].keys()

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_th, paginated_element=adversaries)


# Displays all events in the DB
@bp.route('/explore-events')
def explore_events():

    title='Events'
    events = q.q_get_events.get_events()
    events_th = events[0].keys() #add test for no elements

    return render_template('maps/explore/explore-element.html', title=title, events=events, element_th=events_th, paginated_element=events)


# Displays all tools in the DB
@bp.route('/explore-tools')
def explore_tools():

    title='Tools'
    tools = q.q_get_tools.get_tools()
    tools_th = tools[0].keys() 

    return render_template('maps/explore/explore-element.html', title=title, tools=tools, element_th=tools_th, paginated_element=tools)


# Displays all technique in the DB
@bp.route('/explore-techniques')
def explore_techniques():

    title='Techniques'
    techniques = q.q_get_techniques.get_techniques()
    techniques_th = techniques[0].keys()   

    return render_template('maps/explore/explore-element.html', title=title, techniques=techniques, element_th=techniques_th, paginated_element=techniques)


# Displays all subtechniques in the DB
@bp.route('/explore-subtechniques')
def explore_subtechniques():

    title='Subtechniques'
    subtechniques = q.q_get_subtechniques.get_subtechniques()
    subtechniques_th = subtechniques[0].keys()  

    return render_template('maps/explore/explore-element.html', title=title, techniques=subtechniques, element_th=subtechniques_th, paginated_element=subtechniques)


# DB Analysis Screens

# Display Adversaries per event
@bp.route('/adversaries-x-event')
def get_adversaries_x_event():  

    return render_template('maps/relations/explore-element.html')


# Display Adversaries per suspected origin
@bp.route('/adversaries-x-sorigin')
def get_adversaries_x_sorigin():

    title='Adversaries Suspected Origin'
    adversaries_x_sorigin = q.q_get_adversaries_sorigin.get_adversaries_sorigin()
    adversaries_x_sorigin_th = adversaries_x_sorigin[0].keys()

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=adversaries_x_sorigin)


# Display Adversaries per industry
@bp.route('/adversaries-x-industry')
def get_adversaries_x_industry():    

        return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=adversaries_x_sorigin)


# Display events by industry
@bp.route('/events-x-industry')
def get_events_x_industry():

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=adversaries_x_sorigin)


# Display Techniques per industry
@bp.route('/techniques-per-industry')
def get_techniques_per_industry(): 

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=adversaries_x_sorigin)


# Display Adversaries per tool
@bp.route('/adversaries-x-tool')
def get_adversaries_x_tool(): 
    title='Adversaries per tool'

    adversaries_x_tool = q.q_get_adversaries_x_tool.get_adversaries_x_tool()
    adversaries_x_tool_th = adversaries_x_tool[0].keys()

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_tool_th, paginated_element=adversaries_x_tool) 


# Display Adversaries per technique
@bp.route('/adversaries-x-technique')
def get_adversaries_x_technique():

    title = 'Adversaries per technique'

    adversaries_x_technique = q.q_get_adversaries_x_technique.get_adversaries_x_technique()
    adversaries_x_technique_th = adversaries_x_technique[0].keys()

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_technique_th, paginated_element=adversaries_x_technique)


# Display Tools per techniques
@bp.route('/tools-x-techniques')
def get_tools_x_techniques():

    title = 'Tools per technique'

    tools_x_techniques = q.q_get_tools_x_techniques.get_tools_x_techniques()
    tools_x_techniques_th = tools_x_techniques[0].keys()  

    pagination_tools_x_techniques, page, per_page, offset, pagination = calculate_pagination(tools_x_techniques)

    return render_template('maps/explore/explore-element.html', title=title, element_th=tools_x_techniques_th, paginated_element=tools_x_techniques)


# Display Most used techniques
@bp.route('/most-used-technique')
def get_most_used_techniques():    

    title = 'Most used techniques'

    most_used_techniques = q.q_get_most_used_techniques.get_most_used_techniques()
    most_used_techniques_th = most_used_techniques[0].keys()

    return render_template('maps/explore/explore-element.html', title=title, element_th=most_used_techniques_th, paginated_element=most_used_techniques)


# Creates the new event in the database
@bp.route('/create-events', methods=('GET', 'POST'))
@login_required
def create_event():

    return render_template('maps/creation/create-adversary.html')


# DB INTERACTION FROM FRONT-END

@bp.route('/edit/<title>/<element>', methods=('GET', 'POST'))
def edit_element(): 



    return render_template('maps/creation/create-adversary.html', countries_list=countries_list)

@bp.route('/create-adversary', methods=('GET', 'POST'))
@login_required
def create_adversary():
    
    countries_list = q.q_get_countries.get_countries()


    if request.method == "POST":
        adversary_id = request.form['id']
        adversary_name = request.form['name']
        adversary_description = request.form['description']
        adversary_identifiers = request.form['identifiers']
        adversary_origin = request.form['origin']
        error = None

        if not adversary_name:
            error = 'Adversary name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO adversaries (adversary_id, adversary_name, adversary_description, adversary_identifiers, adversary_sorigin, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (adversary_id, adversary_name, adversary_description, adversary_identifiers, adversary_origin, g.user['id'])
            )
            db.commit()
            return redirect(url_for('maps.create_adversary')) #add success/error message

    return render_template('maps/creation/create-adversary.html', countries_list=countries_list)


# Creates the new tool in the database
@bp.route('/create-tool', methods=('GET', 'POST'))
@login_required
def create_tool():

    if request.method == "POST":
        tool_id = request.form['id']
        tool_name = request.form['name']
        tool_description = request.form['description']
        tool_identifiers = request.form['identifiers']
        error = None

        if not tool_name:
            error = 'Tool name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tools (tool_id, tool_name, tool_description, tool_description, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (tool_id, tool_name, tool_description, tool_description, g.user['id'])
            )
            db.commit()
            return redirect(url_for('maps.create_tool'))

    return render_template('maps/creation/create-tool.html')


# Creates the new technique in the database
@bp.route('/create-technique', methods=('GET', 'POST'))
@login_required
def create_technique():

    tactics_list = q.q_get_tactics.get_tactics()


    if request.method == "POST":

        technique_id = request.form['id']
        technique_name = request.form['name']
        technique_description = request.form['description']
        unprocessed_tactic = request.form['tactic']
        processed_tactic_str =request.form['tactic'].replace('\'','\"') 
        technique_tactic = json.loads(processed_tactic_str) 
        tactic = technique_tactic['Name']

        error = None

        if not technique_name:
            error = 'Adversary name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            result = db.execute(
                'INSERT INTO techniques (technique_id, technique_name, technique_description, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (technique_id, technique_name, technique_description, g.user['id'])
            )
            db.commit()
            technique_db_id = result.lastrowid


            tactic_id = q.q_get_element_id.get_element_id('tactics', 'tactic_name', tactic)
            q_insert_tactic_x_technique.insert_tactic_x_technique(tactic_id, technique_db_id)

            return redirect(url_for('maps.create_technique')) #add success alternative


    return render_template('maps/creation/create-technique.html', tactics_list=tactics_list)


# Creates the new subtechnique in the database
@bp.route('/create-subtechnique', methods=('GET', 'POST'))
def create_subtechnique():

    techniques_list = q.q_get_techniques.get_techniques()
    
    if request.method == "POST":

        subtechnique_id = request.form['id']
        subtechnique_name = request.form['name']
        subtechnique_description = request.form['description']
        unprocessed_technique = request.form['techniques']
        processed_technique_str =request.form['tactic'].replace('\'','\"') 
        subtechnique_technique = json.loads(processed_tactic_str) 
        technique = subtechnique_technique['Name']
        error = None

        if not adversary_name:
            error = 'Adversary name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            result = db.execute(
                'INSERT INTO subtechniques (subtechnique_id, subtechnique_name, subtechnique_description, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (technique_id, technique_name, technique_description, g.user['id'])
            )
            db.commit()
            subtechnique_db_id = result.lastrowid


            technique_id = q.q_get_element_id.get_element_id('techniques', 'technique_name', technique)
            insert_into_table = q.q_insert_relation_into_tables.insert_relation_into_tables('techniques_x_subtechniques', 'technique_id', 'subtechnique_id', technique_id, subtechnique_db_id)

            return redirect(url_for('maps.create_subtechnique')) #add success alternative

    return render_template('maps/creation/create-subtechnique.html', techniques_list=techniques_list)


# Loading ATT&CK to DB for the first time
@bp.route('/first-time')
@login_required
def first_time():
    
    print('Interacting with ATTACKCTI...')
    processor.get_elements()

    return render_template('maps/completed.html')


# Edit DB functions
@bp.route('/edit/<element>')
def edit_database(): 

    return render_template('maps/edit.html')


# Export Results
@bp.route('/export')
def export_file(): 

    return True


# Navigator Functions

# Download SVG
@bp.route('/svg')
def download_svg(): 

    return True

# Open Navigator
@bp.route('/open-in-nav')
def open_in_nav(): 

    return True