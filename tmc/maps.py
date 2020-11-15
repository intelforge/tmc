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

bp = Blueprint('maps', __name__)

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


def get_paginated(element, offset=0, per_page=10):
    return element[offset: offset + per_page]

def calculate_pagination(element):

    total = len(element)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_element = get_paginated(element, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return pagination_element, page, per_page, offset, pagination

# Displays all adversaries in the DB
@bp.route('/explore-adversaries')
def explore_adversaries():

    title='Adversaries'
    adversaries = q.q_get_adversaries.get_adversaries()
    adversaries_th = adversaries[0].keys()
    pagination_adversaries, page, per_page, offset, pagination = calculate_pagination(adversaries)

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_th, paginated_element=pagination_adversaries, page=page, per_page=per_page, pagination=pagination)


# Displays all events in the DB
@bp.route('/explore-events')
def explore_events():

    title='Events'
    events = q.q_get_events.get_events()
    events_th = events[0].keys() #add test for no elements

    pagination_events, page, per_page, offset, pagination = calculate_pagination(events)

    return render_template('maps/explore/explore-element.html', title=title, events=events, element_th=events_th, paginated_element=pagination_events, page=page, per_page=per_page, pagination=pagination)


# Displays all tools in the DB
@bp.route('/explore-tools')
def explore_tools():

    title='Tools'
    tools = q.q_get_tools.get_tools()
    tools_th = tools[0].keys()   

    pagination_tools, page, per_page, offset, pagination = calculate_pagination(tools)

    return render_template('maps/explore/explore-element.html', title=title, tools=tools, element_th=tools_th, paginated_element=pagination_tools, page=page, per_page=per_page, pagination=pagination)


# Displays all technique in the DB
@bp.route('/explore-techniques')
def explore_techniques():

    title='Techniques'
    techniques = q.q_get_techniques.get_techniques()
    techniques_th = techniques[0].keys()   

    pagination_techniques, page, per_page, offset, pagination = calculate_pagination(techniques)

    return render_template('maps/explore/explore-element.html', title=title, techniques=techniques, element_th=techniques_th, paginated_element=pagination_techniques, page=page, per_page=per_page, pagination=pagination)


# Displays all subtechniques in the DB
@bp.route('/explore-subtechniques')
def explore_subtechniques():

    title='Subtechniques'
    subtechniques = q.q_get_subtechniques.get_subtechniques()
    subtechniques_th = subtechniques[0].keys()  

    pagination_subtechniques, page, per_page, offset, pagination = calculate_pagination(subtechniques)

    return render_template('maps/explore/explore-element.html', title=title, techniques=subtechniques, element_th=subtechniques_th, paginated_element=pagination_subtechniques, page=page, per_page=per_page, pagination=pagination)


# DB Analysis Screens

# Display Adversaries per event
@bp.route('/adversaries-x-event')
def get_adversaries_x_event():  

    return render_template('maps/relations/adversaries-x-event.html')


# Display Adversaries per suspected origin
@bp.route('/adversaries-x-sorigin')
def get_adversaries_x_sorigin():

    title='Adversaries Suspected Origin'
    adversaries_x_sorigin = q.q_get_adversaries_sorigin.get_adversaries_sorigin()
    adversaries_x_sorigin_th = adversaries_x_sorigin[0].keys()

    pagination_adversaries_x_sorigin, page, per_page, offset, pagination = calculate_pagination(adversaries_x_sorigin)

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=pagination_adversaries_x_sorigin, page=page, per_page=per_page, pagination=pagination)


# Display Adversaries per industry
@bp.route('/adversaries-x-industry')
def get_adversaries_x_industry():    

        return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=pagination_adversaries_x_sorigin, page=page, per_page=per_page, pagination=pagination)


# Display events by industry
@bp.route('/events-x-industry')
def get_events_x_industry():

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=pagination_adversaries_x_sorigin, page=page, per_page=per_page, pagination=pagination)


# Display Techniques per industry
@bp.route('/techniques-per-industry')
def get_techniques_per_industry(): 

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=pagination_adversaries_x_sorigin, page=page, per_page=per_page, pagination=pagination)


# Display Adversaries per tool
@bp.route('/adversaries-x-tool')
def get_adversaries_x_tool(): 
    title='Adversaries per tool'

    adversaries_x_tool = q.q_get_adversaries_x_tool.get_adversaries_x_tool()
    adversaries_x_tool_th = adversaries_x_tool[0].keys()

    pagination_adversaries_x_tool, page, per_page, offset, pagination = calculate_pagination(adversaries_x_tool)

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_tool_th, paginated_element=pagination_adversaries_x_tool, page=page, per_page=per_page, pagination=pagination)


# Display Adversaries per technique
@bp.route('/adversaries-x-technique')
def get_adversaries_x_technique():

    title = 'Adversaries per technique'

    adversaries_x_technique = q.q_get_adversaries_x_technique.get_adversaries_x_technique()
    adversaries_x_technique_th = adversaries_x_technique[0].keys()

    pagination_adversaries_x_technique, page, per_page, offset, pagination = calculate_pagination(adversaries_x_technique)

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_technique_th, paginated_element=pagination_adversaries_x_technique, page=page, per_page=per_page, pagination=pagination)


# Display Tools per techniques ---------- This query needs an OFFSET
@bp.route('/tools-x-techniques')
def get_tools_x_techniques():

    title = 'Tools per technique'

    tools_x_techniques = q.q_get_tools_x_techniques.get_tools_x_techniques()
    tools_x_techniques_th = tools_x_techniques[0].keys()  

    pagination_tools_x_techniques, page, per_page, offset, pagination = calculate_pagination(tools_x_techniques)

    return render_template('maps/explore/explore-element.html', title=title, element_th=tools_x_techniques_th, paginated_element=pagination_tools_x_techniques, page=page, per_page=per_page, pagination=pagination)


# Display Most used techniques
@bp.route('/most-used-technique')
def get_most_used_techniques():    

    title = 'Most used techniques'

    most_used_techniques = q.q_get_most_used_techniques.get_most_used_techniques()
    most_used_techniques_th = most_used_techniques[0].keys()

    pagination_most_used_techniques, page, per_page, offset, pagination = calculate_pagination(most_used_techniques)

    return render_template('maps/explore/explore-element.html', title=title, element_th=most_used_techniques_th, paginated_element=pagination_most_used_techniques, page=page, per_page=per_page, pagination=pagination)


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


# Creates the new event in the database
@bp.route('/create-events', methods=('GET', 'POST'))
@login_required
def create_event():

    return render_template('maps/creation/create-adversary.html')


# DB INTERACTION FROM FRONT-END

# Creates the new adversary in the database
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
                'INSERT INTO adversaries (adversary_name, adversary_description, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('maps.create_adversary'))

    return render_template('maps/creation/create-adversary.html', countries_list=countries_list)


# Creates the new tool in the database
@bp.route('/create-tool', methods=('GET', 'POST'))
@login_required
def create_tool():
    techniques_list = q.q_get_techniques.get_techniques()
    subtechniques_list = q.q_get_subtechniques.get_subtechniques()

    if request.method == "POST":
        tool_id = request.form['id']
        tool_name = request.form['name']
        tool_description = request.form['description']
        technique = request.form['technique']
        subtechnique = request.form['subtechnique']
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

    return render_template('maps/creation/create-tool.html', techniques_list=techniques_list, subtechniques_list=subtechniques_list)


# Creates the new technique in the database
@bp.route('/create-technique', methods=('GET', 'POST'))
@login_required
def create_technique():

    tactics_list = q.q_get_tactics.get_tactics()


    if request.method == "POST":

        technique_id = request.form['id']
        technique_name = request.form['name']
        technique_description = request.form['description']
        technique_tactic = request.form['tactic']
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


    return render_template('maps/creation/create-technique.html', tactics_list=tactics_list)


# Creates the new subtechnique in the database
@bp.route('/create-subtechnique', methods=('GET', 'POST'))
def create_subtechnique():

    techniques_list = q.q_get_techniques.get_techniques()
    
    if request.method == "POST":

        subtechnique_id = request.form['id']
        subtechnique_name = request.form['name']
        subtechnique_description = request.form['description']
        subtechnique_technique = request.form['techniques']
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

    #  insert_into_table = q.q_insert_into_tables.insert_into_tables('subtechniques', subtechnique_related, subtechnique_name, subtechnique_description, subtechnique_related_technique)
    # subtechnique_id=q.q_get_element_id.get_element_id('subtechniques', 'subtechnique_id', subtechnique_attack_id)

    # processor.techniques_x_subtechniques(related_technique, subtechnique_id)

    return render_template('maps/creation/create-subtechnique.html', techniques_list=techniques_list)


# Loading ATT&CK to DB for the first time
@bp.route('/first-time')
@login_required
def first_time():
    
    print('Interacting with ATTACKCTI...')
    processor.get_elements()

    return render_template('maps/completed.html')

# Successful DB update
@bp.route('/completed')
def completed():

    return render_template('maps/completed.html')
