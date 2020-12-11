from flask import (
    g, redirect, render_template, request, url_for
)
from tmc.auth import login_required
from attackcti import attack_client
from tmc.db import get_db
from IPython import embed
import tmc.queries as q
import logging
logging.basicConfig(level=logging.INFO)

# Global variable
lift = ''
lift = attack_client()

# Classes

class Adversary():

    def __init__(self, element):
        super().__init__()
        self.related_tools = lift.get_software_used_by_group(element)
        self.attack_identifiers = ''
        self.attack_id = element['external_references'][0]['external_id']
        self.adversary_name = element['name']

        try:
            self.adversary_description = element['description']
        except KeyError:
            self.adversary_description = ''
        try:
            aliases_list = element['aliases']

            for element in aliases_list:
                self.attack_identifiers += element + '; '

        except KeyError:
            self.attack_identifiers = ''

        self.adversary_id = insert_adversary(self.attack_id, self.adversary_name, self.adversary_description, self.attack_identifiers)


class Events():

    def __init__(self, element):
        super().__init__()


class Tools():

    def __init__(self, element):
        super().__init__()
        self.attack_id = element['external_references'][0]['external_id']
        self.tool_name = element['name']
        try:
            self.tool_description = element['description']
        except KeyError:
            self.tool_description = ''
        try:
            self.attack_identifiers = element['x_mitre_aliases']
        except KeyError:
            self.attack_identifiers = ''
        self.techniques_used = lift.get_techniques_used_by_software(element)
        self.tool_id = insert_tool(self.attack_id, self.tool_name, self.tool_description)


class Tactics():

    def __init__(self, element):
        super().__init__()
        self.attack_id = element['external_references'][0]['external_id']
        self.tactic_name = element['name']
        self.tactic_description = element['description']
        self.tactic_id = insert_tactic(self.attack_id, self.tactic_name, self.tactic_description)


class Techniques():

    def __init__(self, element):
        super().__init__()
        self.attack_id = element['external_references'][0]['external_id']

        if '.' in self.attack_id:
            technique_attack_id,subtechnique_attack_id = self.attack_id.split('.', 1)
            sub = Subtechniques(element, self.attack_id)

        self.technique_name = element['name']
        self.technique_description = element['description']
        self.related_tactic = element['kill_chain_phases'][0]['phase_name']
        self.technique_id = insert_technique(self.attack_id, self.technique_name, self.technique_description)


class Subtechniques():

    def __init__(self, element, subtechnique_attack_id):
        super().__init__()
        self.attack_id = subtechnique_attack_id
        self.subtechnique_name = element['name']
        self.subtechnique_description = element['description']
        self.related_tactic = element['kill_chain_phases'][0]['phase_name']
        self.subtechnique_id = insert_subtechnique(self.attack_id, self.subtechnique_name, self.subtechnique_description)


# ATT&CK FRAMEWORK INTERACTION 
def get_elements():

    tactics = lift.get_tactics()
    for element in tactics:

        if 'x_mitre_deprecated' in element:
            continue
        else:
            tac = Tactics(element)

    unsorted_techniques = lift.get_techniques()
    techniques = sorted(unsorted_techniques, key = lambda i: i['external_references'][0]['external_id'])
    for element in techniques:

        if element['revoked'] == True:
            continue
  
        technique_id = element['external_references'][0]['external_id']

        if '.' in technique_id:
            subtec = Subtechniques(element, technique_id)
            technique_attack_id,subtechnique_attack_id = technique_id.split('.', 1)
            related_technique=q.q_get_element_id.get_element_id('techniques', 'technique_id', technique_attack_id)
            insert_tecxsubtec(related_technique, subtec.subtechnique_id)
        else:
            tec = Techniques(element)
            insert_tacxtec(tec.technique_id, tec.related_tactic)

    tools = lift.get_software()
    for element in tools:
        t = Tools(element)
        insert_toolxtec(t.tool_name, t.tool_id, t.techniques_used)

    adversaries = lift.get_groups()
    for element in adversaries:
        adv = Adversary(element)
        insert_advxtool(adv.adversary_id, adv.related_tools)


def insert_tactic(attack_id, tactic_name, tactic_description):

    existence = q.q_get_element_id.get_element_id('tactics', 'tactic_name', tactic_name)
    if not existence:
        insert_into_table = q.q_insert_into_tables.insert_into_tables('tactics', attack_id, tactic_name, tactic_description)
        logging.info('Created tactic %s' % tactic_name)
        return insert_into_table
    else:
        return existence


# Adding ATT&CK Techniques
def insert_technique(attack_id, technique_name, technique_description):

    insert_into_table = q.q_insert_into_tables.insert_into_tables('techniques', attack_id, technique_name, technique_description)
    logging.info('Created technique %s' % technique_name)
    return insert_into_table


#REFACTOR THIS
def insert_subtechnique(attack_id, subtechnique_name, subtechnique_description):

    insert_into_table = q.q_insert_into_tables.insert_into_tables('subtechniques', attack_id, subtechnique_name, subtechnique_description)
    logging.info('Created technique %s' % subtechnique_name)
    return insert_into_table


# Adding ATT&CK Adversaries
def insert_adversary(attack_id, adversary_name, adversary_description, attack_identifiers):

    insert_into_table = q.q_insert_adversary_into_tables.insert_adversary_into_tables('adversaries', attack_id, adversary_name, adversary_description, attack_identifiers)
    logging.info('Created adversary %s' % adversary_name)
    return insert_into_table


# Adding ATT&CK Tools
def insert_tool(attack_id, tool_name, tool_description):

    insert_into_table = q.q_insert_into_tables.insert_into_tables('tools', attack_id, tool_name, tool_description)
    logging.info('Created tool %s' % tool_name)
    return insert_into_table


# Insert Tools x Techniques ----- this is gatherin technique att&ck id, instead of technique id
def insert_toolxtec(tool_name, tool_id, techniques_used): 

    for element in techniques_used:

        technique_attack_id = element['external_references'][0]['external_id']

        if '.' in technique_attack_id:
            subtechnique_id = q.q_get_element_id.get_element_id('subtechniques', 'subtechnique_id', technique_attack_id)
            result = q.q_insert_tool_x_subtechn.insert_tool_x_subtechn('tools_x_subtechniques', tool_id, subtechnique_id)
    
        else:
            technique_id = q.q_get_element_id.get_element_id('techniques', 'technique_id', technique_attack_id)
            result = q.q_insert_tool_x_techn.insert_tool_x_techn('tools_x_techniques', tool_id, technique_id)
        logging.info('Created relationship for %s' % tool_name)
    return result



# Adding ATT&CK TacticxTechniques
def insert_tacxtec(technique_id, related_tactic):

    error = []
    tactic = related_tactic.replace('-', ' ')

    if 'ics' in tactic:
        tactic=tactic.replace(' ics', '')

    tactic_id = q.q_get_element_id.get_element_id('tactics', 'tactic_name', tactic)

    if tactic_id == 0:
        logging.info('Deprecated tactic in %s: ' % technique_id)
    else:
        try:
            tactic_x_technique = q.q_insert_tactic_x_technique.insert_tactic_x_technique(tactic_id, technique_id)
            logging.info('Created tactic relationship')
        except KeyError:
             logging.info('Raised KeyError exception with tactic in %s: ' % technique_id)


# Insert relation insert_advxtool
def insert_advxtool(adversary_id, related_tools):
    
    for tool in related_tools:
        tool_attack_id = tool['external_references'][0]['external_id']
        tool_id = q.q_get_element_id.get_element_id('tools', 'tool_id', tool_attack_id)

        result = q.q_insert_adversary_x_tool.insert_adversary_x_tool(adversary_id, tool_id)
        logging.info('Created adversary per tool relationship')    
    return result


# Insert Subtechniques x Techniques
def insert_tecxsubtec(related_technique, subattack_id):
    
    insert_into_table = q.q_insert_relation_into_tables.insert_relation_into_tables('techniques_x_subtechniques', 'technique_id', 'subtechnique_id', related_technique, subattack_id)
    logging.info('Created technique per subtechnique relationship')
    return insert_into_table
