from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from tmc.auth import login_required
from tmc.db import get_db
from IPython import embed
import tmc.queries as q
from tmc.queries import *
from random import random
import tmc.processor as processor
import tmc.config as config
import time
import json
import ast
import requests
import csv
import os
import uuid 
import urllib


bp = Blueprint('maps', __name__, template_folder='templates')


# Loading ATT&CK to DB for the first time
@bp.route('/first-time')
@login_required
def first_time():
    
    print('Interacting with ATTACKCTI...')
    processor.get_elements()
    message="You can now start exploring the database."

    return render_template('maps/completed.html', message=message)


# Homepage
@bp.route('/', methods=["GET", "POST"])
def index():

    adversaries_list = q.q_get_adversaries.get_adversaries()
    tools_list = q.q_get_tools.get_tools()
    industries_list = q.q_get_industries.get_industries()

    return render_template('maps/welcome.html', adversaries_list=adversaries_list, tools_list=tools_list, industries_list=industries_list)


@bp.route('/tram-interaction', methods=["GET", "POST"])
def tram_mapping():

    if request.method == "POST":

        req = request.form
        adversary_dict = ast.literal_eval(req['adversary']) # convert string dict into real dict
        adversary = adversary_dict['db_id']
        tool_dict = ast.literal_eval(req['tool']) # convert string dict into real dict
        tool = tool_dict['db_id']
        industry_dict = ast.literal_eval(req['industry']) # convert string dict into real dict
        industry = industry_dict['db_id']
        event_name = req['event_name']
        event_description = req['event_description']
        event_url = req['url']

        # Creates the security event and all its relationships
        event = q.q_insert_into_events.insert_into_events(event_name, event_description, event_url)
        adv_x_event = q.q_insert_adversary_x_event.insert_adversary_x_event(adversary, event)
        event_x_ind = q.q_insert_event_x_industry.insert_event_x_industry(event, industry)
        # Sends the URL provided to TRAM for mapping
        tram_id=str(tool)+'_'+event_name
        print(tram_id)
        send_url_to_tram(tram_id, event_url)
        message = 'Please complete TRAM workflow before continuing. TMC will automatically process TRAM mapping when done. Please wait before continuing..'

        return render_template('maps/completed.html', message=message)


# Issues POST request to TRAM with the report URL you want to process
def send_url_to_tram(tram_id, event_url):

    tram_insert = {
        "index":"insert_report",
        "url": [event_url],
        "title": [tram_id],
        "request": True
    }
    url = config.config_dict['tram'] + "/rest"
    requests.post(url=url, json=tram_insert, headers={"content-type":"application/json"})


# Process the techniques sent by TRAM issued POST request after analysis completion
@bp.route('/tram-response', methods=['GET', 'POST']) 
def wait_tram_response():
    
    if request.method == 'POST':
        tram_response = json.loads(request.data)
        print(tram_response)

        try:

            tool_id = tram_response[0]['title'].split('_')[0]

            for element in tram_response:
                if '.' in element['attack_tid']:
                    subtechnique_attack_id = element['attack_tid']
                    db_id = q.q_get_element_id.get_element_id('subtechniques', 'subtechnique_id', subtechnique_attack_id)
                    tool_x_techniques = q_insert_tool_x_subtechn.insert_tool_x_subtechn('tools_x_subtechniques', tool_id, db_id)
                else:
                    technique_attack_id = element['attack_tid']
                    db_id = q.q_get_element_id.get_element_id('techniques', 'technique_id', technique_attack_id)
                    tools_x_subtechniques = q.q_insert_tool_x_techn.insert_tool_x_techn('tools_x_techniques', tool_id, db_id)
            
            message="Tram interaction has been completed. You can now explore your mapping in the TMC."

        except IndexError:
            message="TMC did not expcet a TRAM request for this report."
    
    return render_template('maps/completed.html', message=message)

# Navigator Functions


# Open Navigator
@bp.route('/nav/<element>/<element_id>') 
def open_in_nav(element, element_id): 
    nav_dict = {
       "name":"Threat Mapping Catalogue",
        "versions": {
        "attack": "8",
        "navigator": "4.0",
        "layer": "4.0"
        },
       "description": element + " related techniques",
       "domain":"mitre-enterprise",
       "gradient":{
          "colors":[
             "#778ca3",
             "#778ca3"
          ],
          "minValue":0,
          "maxValue":100
       },
       "legendItems":[
          {
             "label":"Has at least one test",
             "color":"#ce232e"
          }
       ],
       "techniques":[]
       }

    element_techniques = ''

    # Both queries bring techniques & subtechniques
    if element == 'adversary':
        element_techniques = q_get_adversaries_techniques.get_adversaries_techniques(element_id)
    elif element == 'tool':
        element_techniques = q_get_tool_techniques.get_tool_techniques(element_id)

    for technique in element_techniques:
        if technique['Subtechnique ID']:
            new_technique = {
                "techniqueID": technique['Subtechnique ID'],
                "score":100,
                "enabled":True
                }
        else:
            new_technique = {
                "techniqueID": technique['Technique ID'],
                "score":100,
                "enabled":True
                }

        nav_dict['techniques'].append(new_technique)

    # Creates a json file with the retrieved information from the database
    filename = create_nav_file(nav_dict, element, element_id)
    # Creates the url with the path to the created file to send it to the navigator 
    encoded_path = urllib.parse.quote_plus(str(config.config_dict['tmc'])+'/static/export/'+str(filename))
    encoded_url = str(config.config_dict['navigator']+'/fetch/'+encoded_path)

    return redirect(encoded_url)


def create_nav_file(nav_dict, element, element_id):
    filename = element + '_' + str(element_id) + '_' + str(uuid.uuid1()) + '.json'
    directory = os.path.dirname(os.path.realpath(__file__)) + '/static/export/'
    filepath = directory + filename

    with open(filepath, 'w+') as fh:
        json.dump(nav_dict, fh)
    fh.close()

    return filename

# Export Results
@bp.route('/export/<element>/<element_id>')
def export_file(element, element_id): 

    # Both queries bring techniques & subtechniques
    if element == 'adversary':
        element_techniques = q_get_adversaries_techniques.get_adversaries_techniques(element_id)
        create_csv_file(element_techniques, element, element_id)
    elif element == 'tool':
        element_techniques = q_get_tool_techniques.get_tool_techniques(element_id)
        create_csv_file(element_techniques, element, element_id)

    return render_template('maps/explore/main.html') 

def create_csv_file(element_techniques, element, element_id):
    
    headers = 'Tool \t Technique ID \t Technique \t Subtechnique ID \t Subtechnique'
    filename = element + '_' + str(element_id) + '_techniques_mapped_' + str(uuid.uuid1()) +'.csv'
    parent = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    filepath = parent + '/export/' + filename


    with open(filepath, 'w+', newline='') as new_file:
        new_file.write(headers +'\n')
        for line in element_techniques:
            for key, value in line.items():
                new_file.write(str(value) + '\t')
            new_file.write('\n')
    new_file.close()



# Download SVG
@bp.route('/svg/<element>/<element_id>')
def download_svg(element, element_id): 

    # Both queries bring techniques & subtechniques
    if element == 'adversary':
        element_techniques = q_get_adversaries_techniques.get_adversaries_techniques(element_id)
    elif element == 'tool':
        element_techniques = q_get_tool_techniques.get_tool_techniques(element_id)


    return render_template('maps/explore/main.html') 


# List all posible actions to display data
@bp.route('/explore')
def explore():

    return render_template('maps/explore/main.html') 


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
    try:
        events_th = events[0].keys() #add test for no elements
    except IndexError:
        return render_template('maps/no-data.html')
    else:
        return render_template('maps/explore/explore-element.html', title=title, events=events, element_th=events_th, paginated_element=events)


# Displays all tools in the DB
@bp.route('/explore-tools')
def explore_tools():

    title='Tools'
    tools = q.q_get_tools.get_tools()
    tools_th = tools[0].keys() 

    return render_template('maps/explore/explore-element.html', title=title, tools=tools, element_th=tools_th, paginated_element=tools)


# Displays all tactics in the DB
@bp.route('/explore-tactics')
def explore_tactics():

    title='Tactics'
    tactics = q.q_get_tactics.get_tactics()
    tactics_th = tactics[0].keys()   

    return render_template('maps/explore/explore-element.html', title=title, tactics=tactics, element_th=tactics_th, paginated_element=tactics)


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
    adversaries_x_event = ''

    if not adversaries_x_event:
        return render_template('maps/no-data.html')

    return render_template('maps/relations/explore-element.html')


# Display Adversaries per suspected origin
@bp.route('/adversaries-x-sorigin')
def get_adversaries_x_sorigin():

    title='Adversaries Suspected Origin'
    adversaries_x_sorigin = q.q_get_adversaries_sorigin.get_adversaries_sorigin()

    try: 
        adversaries_x_sorigin_th = adversaries_x_sorigin[0].keys()

    except IndexError:
        return render_template('maps/no-data.html')  

    return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=adversaries_x_sorigin)


# Display Adversaries per industry
@bp.route('/adversaries-x-industry')
def get_adversaries_x_industry():  

    adversaries_x_industry = ''
    
    if not adversaries_x_industry:
        return render_template('maps/no-data.html')  

    else:
        return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=adversaries_x_sorigin)


# Display events by industry
@bp.route('/events-x-industry')
def get_events_x_industry():

    events_x_industry = ''
    
    if not events_x_industry:
        return render_template('maps/no-data.html')

    else:
        return render_template('maps/explore/explore-element.html', title=title, element_th=adversaries_x_sorigin_th, paginated_element=adversaries_x_sorigin)


# Display Techniques per industry
@bp.route('/techniques-per-industry')
def get_techniques_per_industry(): 

    techniques_per_industry = ''

    if not techniques_per_industry:
        return render_template('maps/no-data.html')

    else:

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

@bp.route('/create-adversary', methods=('GET', 'POST'))
@login_required
def create_adversary():
    
    countries_list = q.q_get_countries.get_countries()

    if request.method == "POST":
        adversary_id = request.form['adversary_id']
        adversary_name = request.form['adversary_name']
        adversary_description = request.form['description']
        adversary_identifiers = request.form['adversary_identifiers']
        adversary_origin = request.form['sorigin']
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
            message = 'Successfully created Adversary'
            return render_template('maps/completed.html', message=message)

    return render_template('maps/creation/create-adversary.html', countries_list=countries_list, request_adversary = '')


@bp.route('/edit/adversary/<element>', methods=('GET', 'POST'))
def render_edit_adversary(element):

    countries_list = q.q_get_countries.get_countries()
    request_adversary=q.q_get_adversaries.get_adversaries(element)
    request_adversary_techniques=q.q_get_adversaries_techniques.get_adversaries_techniques(element)

    if request_adversary_techniques:
        adversary_techniques_th = request_adversary_techniques[0].keys()
    else:
        adversary_techniques_th = ''

    if request_adversary is False:
        return render_template('maps/404.html')
    else:
        return render_template('maps/creation/create-adversary.html', request_adversary_techniques=request_adversary_techniques, element_th=adversary_techniques_th, request_adversary=request_adversary, countries_list=countries_list)


@bp.route('/edit-adversary', methods=('GET', 'POST'))
@login_required
def edit_adversary():
    try:
        if request.method == 'POST':
            edited = request.form

            db_id = edited['db_id']
            adversary_id = edited['adversary_id']
            adversary_name = edited['adversary_name']
            adversary_identifiers = edited['adversary_identifiers']
            adversary_sorigin = edited['sorigin']
            adversary_description = edited['description']
            updated_date = time.strftime('%Y-%m-%d %H:%M:%S')

            db = get_db()
            db.execute(
                'UPDATE adversaries SET adversary_id=?, adversary_name=?, adversary_description=?, adversary_identifiers=?, adversary_sorigin=?, updated_date=?, updated_by=? WHERE id=?',
                (adversary_id, adversary_name, adversary_description, adversary_identifiers, adversary_sorigin, updated_date, g.user['id'], db_id,)
            )
            db.commit()

            return redirect('/explore-adversaries') 
    except:
        return render_template('maps/404.html')


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
            message = 'Successfully created tool'

            return render_template('maps/completed.html', message=message)

    return render_template('maps/creation/create-tool.html')


@bp.route('/edit/tool/<element>', methods=('GET', 'POST'))
def render_edit_tool(element):

    request_tool=q.q_get_tools.get_tools(element)

# MISSING QUERY HERE

    request_tool_techniques=q.q_get_tool_techniques.get_tool_techniques(element)

    if request_tool_techniques:
        tool_techniques_th = request_tool_techniques[0].keys()
    else:
        tool_techniques_th = ''

    if request_tool is False:
        return render_template('maps/404.html')
    else:
        return render_template('maps/creation/create-tool.html', request_tool_techniques=request_tool_techniques, element_th=tool_techniques_th, request_tool=request_tool)


@bp.route('/edit-tool', methods=('GET', 'POST'))
@login_required
def edit_tool():
    try:
        if request.method == 'POST':
            edited = request.form

            db_id = edited['db_id']
            tool_id = edited['tool_id']
            tool_name = edited['tool_name']
            tool_identifiers = edited['tool_identifiers']
            tool_adversary = edited['tool_adversary']
            tool_description = edited['description']
            updated_date = time.strftime('%Y-%m-%d %H:%M:%S')

            db = get_db()
            db.execute(
                'UPDATE tools SET tool_id=?, tool_name=?, tool_description=?, tool_identifiers=?, updated_date=?, updated_by=? WHERE id=?',
                (tool_id, tool_name, tool_description, tool_identifiers, updated_date, g.user['id'], db_id,)
            )
            db.commit()

            return redirect('/explore-tools') 
    except:
        return render_template('maps/404.html')


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
            message = 'Successfully created technique'

            return render_template('maps/completed.html', message=message)


    return render_template('maps/creation/create-technique.html', tactics_list=tactics_list)


@bp.route('/edit/technique/<element>', methods=('GET', 'POST'))
def render_edit_technique(element):

    request_technique=q.q_get_techniques.get_techniques(element)
    request_related_tools=q.q_get_tools_x_techniques.get_tools_x_techniques(element)

    if request_related_tools:
        request_related_tools_th = request_related_tools[0].keys()
    else:
        request_related_tools_th = ''

    if request_technique is False:
        return render_template('maps/404.html')
    else:
        return render_template('maps/creation/create-technique.html', request_related_tools=request_related_tools, element_th=request_related_tools_th, request_technique=request_technique)


@bp.route('/edit-technique', methods=('GET', 'POST'))
@login_required
def edit_technique():
    try:
        if request.method == 'POST':
            edited = request.form

            db_id = edited['db_id']
            technique_id = edited['technique_id']
            technique_name = edited['technique_name']
            technique_tactic = edited['technique_tactic']
            technique_description = edited['description']
            updated_date = time.strftime('%Y-%m-%d %H:%M:%S')

            db = get_db()
            db.execute(
                'UPDATE tools SET technique_id=?, technique_name=?, technique_description=?, updated_date=?, updated_by=? WHERE id=?',
                (technique_id, technique_name, technique_description, updated_date, g.user['id'], db_id,)
            )
            db.commit()

            return redirect('/explore-techniques') 
    except:
        return render_template('maps/404.html')


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

            message = 'Successfully created Subtechnique'
            return render_template('maps/completed.html', message=message)

    return render_template('maps/creation/create-subtechnique.html', techniques_list=techniques_list)


@bp.route('/edit/subtechnique/<element>', methods=('GET', 'POST'))
def render_edit_subtechnique(element):

    request_subtechnique=q.q_get_subtechniques.get_subtechniques(element)
    request_related_tools=q.q_get_tools_x_subtechniques.get_tools_x_subtechniques(element)

    if request_related_tools:
        request_related_tools_th = request_related_tools[0].keys()
    else:
        request_related_tools_th = ''

    if request_subtechnique is False:
        return render_template('maps/404.html')
    else:
        return render_template('maps/creation/create-subtechnique.html', request_related_tools=request_related_tools, element_th=request_related_tools_th, request_subtechnique=request_subtechnique)


@bp.route('/edit-subtechnique', methods=('GET', 'POST'))
@login_required
def edit_subtechnique():
    try:
        if request.method == 'POST':
            edited = request.form

            db_id = edited['db_id']
            subtechnique_id = edited['subtechnique_id']
            subtechnique_name = edited['subtechnique_name']
            subtechnique_tactic = edited['subtechnique_tactic']
            subtechnique_description = edited['description']
            updated_date = time.strftime('%Y-%m-%d %H:%M:%S')

            db = get_db()
            db.execute(
                'UPDATE techniques SET subtechnique_id=?, subtechnique_name=?, subtechnique_description=?, updated_date=?, updated_by=? WHERE id=?',
                (subtechnique_id, subtechnique_name, subtechnique_description, updated_date, g.user['id'], db_id,)
            )
            db.commit()

            return redirect('/explore-subtechniques') 
    except:
        return render_template('maps/404.html')



@bp.route('/edit/tactic/<element>', methods=('GET', 'POST'))
def render_edit_tactic(element):

    request_tactic=q.q_get_tactics.get_tactics(element)
    request_related_tactics=q.q_get_related_tactics.get_related_tactics(element)

    if request_related_tactics:
        request_tactics_th = request_related_tactics[0].keys()
    else:
        request_related_tactics_th = ''

    if request_tactic is False:
        return render_template('maps/404.html')
    else:
        return render_template('maps/creation/create-adversary.html', request_related_tactics=request_related_tactics, element_th=request_tactics_th, request_tactic=request_tactic)


@bp.route('/edit-tactic', methods=('GET', 'POST'))
@login_required
def edit_tactic():
    try:
        if request.method == 'POST':
            edited = request.form

            db_id = edited['db_id']
            tactic_id = edited['adversary_id']
            tactic_name = edited['adversary_name']
            tactic_description = edited['description']
            updated_date = time.strftime('%Y-%m-%d %H:%M:%S')

            db = get_db()
            db.execute(
                'UPDATE tactics SET tactic_id=?, tactic_name=?, tactic_description=?, updated_date=?, updated_by=? WHERE id=?',
                (tactic_id, tactic_name, tactic_description, updated_date, g.user['id'], db_id,)
            )
            db.commit()

            return redirect('/explore-tactics') 
    except:
        return render_template('maps/404.html')
