from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from tmc.auth import login_required
from tmc.db import get_db
from attackcti import attack_client
from IPython import embed
import tmc.queries as q
from tmc.queries import *

bp = Blueprint('maps', __name__)

# Homepage
@bp.route('/')
def index():

    adversaries_list = q.q_get_adversaries_names.get_adversaries_names()

    return render_template('maps/index.html', adversaries_list=adversaries_list)

# List all posible actions to display data
@bp.route('/explore')
def explore():

    return render_template('maps/explore.html') 


# Displays all adversaries in the DB
@bp.route('/explore-adversaries')
def explore_adversaries():

    adversaries = q.q_get_adversaries.get_adversaries()
    adversaries_th = adversaries[0].keys() 

    return render_template('maps/explore/explore-adversaries.html', adversaries=adversaries, adversaries_th=adversaries_th)


# Displays all campaigns in the DB
@bp.route('/explore-campaigns')
def explore_campaigns():

    # campaigns = q.q_get_campaigns.get_campaigns()
    # campaigns_th = campaigns[0].keys() 

    return render_template('maps/explore/explore-campaigns.html') #, campaigns=campaigns, campaigns_th=campaigns_th)


# Displays all tools in the DB
@bp.route('/explore-tools')
def explore_tools():

    tools = q.q_get_tools.get_tools()
    tools_th = tools[0].keys()   

    return render_template('maps/explore/explore-tools.html', tools=tools, tools_th=tools_th)


# Displays all technique in the DB
@bp.route('/explore-techniques')
def explore_techniques():

    techniques = q.q_get_techniques.get_techniques()
    techniques_th = techniques[0].keys()    

    return render_template('maps/explore/explore-techniques.html', techniques=techniques, techniques_th=techniques_th)


# Displays all subtechniques in the DB
@bp.route('/explore-subtechniques')
def explore_subtechniques():

    # subtechniques = q.q_get_subtechniques.get_subtechniques()
    # subtechniques_th = subtechniques[0].keys()  

    return render_template('maps/explore/explore-subtechniques.html') #, subtechniques=subtechniques, subtechniques_th=subtechniques_th)


# DB Analysis Screens

# Display Adversaries per campaign
@bp.route('/adversaries-x-campaign')
def get_adversaries_x_campaign():  

    return render_template('maps/relations/adversaries-x-campaign.html')


# Display Adversaries per suspected origin
@bp.route('/adversaries-x-sorigin')
def get_adversaries_x_sorigin():  

    return render_template('maps/relations/adversaries-x-sorigin.html')


# Display Adversaries per industry
@bp.route('/adversaries-per-industry')
def get_adversaries_x_industry():    

    return render_template('maps/relations/adversaries-per-industry.html')


# Display Campaigns by industry
@bp.route('/campaigns-x-industry')
def get_campaigns_x_industry():

    return render_template('maps/relations/campaigns-x-industry.html')


# Display Techniques per industry
@bp.route('/techniques-per-industry')
def get_techniques_per_industry(): 

    return render_template('maps/relations/techniques-x-industry.html')


# Display Adversaries per tool ---------- This query needs an OFFSET
@bp.route('/adversaries-x-tool')
def get_adversaries_x_tool(): 

    adversaries_x_tool = q.q_get_adversaries_x_tool.get_adversaries_x_tool()
    adversaries_x_tool_th = adversaries_x_tool[0].keys()  

    return render_template('maps/relations/adversaries-x-tool.html', adversaries_x_tool=adversaries_x_tool, adversaries_x_tool_th=adversaries_x_tool_th)


# Display Adversaries per technique
@bp.route('/adversaries-x-technique')
def get_adversaries_x_technique():

    adversaries_x_technique = q.q_get_adversaries_x_technique.get_adversaries_x_technique()
    adversaries_x_technique_th = adversaries_x_technique[0].keys()  

    return render_template('maps/relations/adversaries-x-technique.html', adversaries_x_technique=adversaries_x_technique, adversaries_x_technique_th=adversaries_x_technique_th)


# Display Tools per techniques ---------- This query needs an OFFSET
@bp.route('/tools-x-techniques')
def get_tools_x_techniques():

    tools_x_techniques = q.q_get_tools_x_techniques.get_tools_x_techniques()
    tools_x_techniques_th = tools_x_techniques[0].keys()  

    return render_template('maps/relations/tools-x-technique.html', tools_x_techniques=tools_x_techniques, tools_x_techniques_th=tools_x_techniques_th)


# Display Most used techniques
@bp.route('/most-used-technique')
def get_most_used_techniques():    

    most_used_techniques = q.q_get_most_used_techniques.get_most_used_techniques()
    most_used_techniques_th = most_used_techniques[0].keys()

    return render_template('maps/relations/most-used-technique.html', most_used_techniques=most_used_techniques, most_used_techniques_th=most_used_techniques_th)


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

        insert_into_table = q.q_insert_into_tables.insert_into_tables('tactics', tactic_id, tactic_name, tactic_description)
        print('Created tactic %s' % tactic_name)

    return redirect(url_for('maps.completed'))


# Adding ATT&CK Techniques
@bp.route('/attackcti_techniques', methods=('GET', 'POST'))
@login_required
def get_techniques():
    lift = attack_client()
    unsorted_techniques = lift.get_techniques()
    techniques = sorted(unsorted_techniques, key = lambda i: i['external_references'][0]['external_id'])
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

            if '.' in technique_id:
                print('entre al if')
                create_subtechnique(technique_id, technique_name, technique_description, '')
            else:
                insert_into_table = q.q_insert_into_tables.insert_into_tables('techniques', technique_id, technique_name, technique_description)
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
    error = []

    for element in techniques:
        technique_name = element['name']
        technique_attack_id = element['external_references'][0]['external_id']
        technique_id = q.q_get_element_id.get_element_id('techniques', 'technique_id', technique_attack_id)

        try:
            technique_tactic = element['kill_chain_phases'][0]['phase_name']
            tactic_id = q.q_get_element_id.get_element_id('tactics', 'tactic_name', technique_tactic)

            tactic_x_technique = q.q_insert_tactic_x_technique.insert_tactic_x_technique(tactic_id, technique_id)
            print('Created tactic relationship')
        except KeyError:
            error.append(tactic_id)

    return redirect(url_for('maps.completed'))


# Adding ATT&CK Adversaries
@bp.route('/attackcti_groups', methods=('GET', 'POST'))
@login_required
def get_groups():
    lift = attack_client()
    groups = lift.get_groups()

    for element in groups:
        group_identifiers = ''
        group_id = element['external_references'][0]['external_id']
        group_name = element['name']

        try:
            group_description = element['description']
        except KeyError:
            group_description = ''
        try:
            aliases_list = element['aliases']

            for element in aliases_list:
                group_identifiers += element + '; '

        except KeyError:
            group_identifiers = ''

        insert_into_table = q.q_insert_adversary_into_tables.insert_adversary_into_tables('adversaries', group_id, group_name, group_description, group_identifiers)

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
            tool_identifiers = element['x_mitre_aliases']
        except KeyError:
            tool_identifiers = ''

        insert_into_table = q.q_insert_into_tables.insert_into_tables('tools', tool_id, tool_name, tool_description)

    return redirect(url_for('maps.completed'))


# DB INTERACTION FROM FRONT-END

# Creates the new subtechnique in the database
@bp.route('/create-subtechnique', methods=('GET', 'POST'))
def create_subtechnique(technique_id, subtechnique_name, subtechnique_description, *related_technique):

    subtechnique_attack_id = ''
    technique_attack_id = ''

    if '.' in technique_id: 
        technique_attack_id,subtechnique_attack_id = technique_id.split('.', 1)
        related_technique=q.q_get_element_id.get_element_id('techniques', 'technique_id', technique_attack_id)

    insert_into_table = q.q_insert_into_tables.insert_into_tables('subtechniques', subtechnique_attack_id, subtechnique_name, subtechnique_description)
    subtechnique_id=q.q_get_element_id.get_element_id('subtechniques', 'subtechnique_id', subtechnique_attack_id)

    techniques_x_subtechniques(related_technique, subtechnique_id)

    return redirect(url_for('maps.completed'))
    #return render_template('maps/creation/create-subtechnique.html')


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

    return render_template('maps/creation/create-adversary.html')


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

    return render_template('maps/creation/create-tool.html')


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

        if error:
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

    return render_template('maps/creation/create-technique.html')


# Insert Subtechniques x Techniques
@bp.route('/subtechxtech', methods=('GET', 'POST'))
def techniques_x_subtechniques(related_technique, subtechnique_id):
    
    insert_into_table = q.q_insert_relation_into_tables.insert_relation_into_tables('techniques_x_subtechnique', related_technique, subtechnique_id)

    return True


# Insert Tools x Techniques
@bp.route('/attackcti_toolxtech', methods=('GET', 'POST'))
@login_required
def tool_x_technique():
    lift = attack_client()
    tools = lift.get_software()
    
    for element in tools:
        tool_attack_id = element['external_references'][0]['external_id']
        tool_id = q.q_get_element_id.get_element_id('tools', 'tool_id', tool_attack_id)
        techniques_used = lift.get_techniques_used_by_software(element)

        for technique in techniques_used:
            technique_attack_id = technique['external_references'][0]['external_id']
            technique_id = q.q_get_element_id.get_element_id('techniques', 'technique_id', technique_attack_id)
            
            result = q.q_insert_tool_x_techn.insert_tool_x_techn(tool_id, technique_id)

    return True


# Insert relation adversary_x_tool
@bp.route('/attackcti_advxtool', methods=('GET', 'POST'))
@login_required
def adversary_x_tool():
    lift = attack_client()
    groups = lift.get_groups()
    
    for element in groups:
        adversary_attack_id = element['external_references'][0]['external_id']
        adversary_id = q.q_get_element_id.get_element_id('adversaries', 'adversary_id', adversary_attack_id)
        adversary = element['name']

        tools_used = lift.get_software_used_by_group(element)

        for tool in tools_used:
            tool_attack_id = tool['external_references'][0]['external_id']
            tool_id = q.q_get_element_id.get_element_id('tools', 'tool_id', tool_attack_id)

            result = q.q_insert_adversary_x_tool.insert_adversary_x_tool(adversary_id, tool_id)
        
    return True


# Creates the new campaign in the database
@bp.route('/create-campaign', methods=('GET', 'POST'))
@login_required
def create_campaign():

    return render_template('maps/creation/create-adversary.html')


# Loading ATT&CK to DB for the first time
@bp.route('/first-time')
def first_time():
    
    print('Inserting tactics...')
    get_tactics()

    print('Inserting techniques...')
    get_techniques()
    
    print('Inserting groups...')
    get_groups()
    
    print('Inserting tools...')
    get_tools()
    
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
