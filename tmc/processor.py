from flask import (
    g, redirect, render_template, request, url_for
)
from tmc.auth import login_required
from attackcti import attack_client
from tmc.db import get_db
from IPython import embed
import tmc.queries as q

# Global variable
lift = attack_client()

# Classes

class Adversary():

    def __init__(self, element):
        super().__init__()
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
        self.related_tools = lift.get_software_used_by_group(element)
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

        try:
            self.technique_description = element['description']
        except KeyError:
            self.technique_description = ''

        try:
            self.related_tactic = element['kill_chain_phases'][0]['phase_name']
        except KeyError:
            self.related_tactic = ''
            error = []
            error.append(self.attack_id)
            # MOBILE TECHNIQUES MISSING TACTIC REFERENCE:
            #T1443, T1425, T1442, T1419, T1440, T1462, T1460, T1459, T1457, T1445, T1431, T1434, T1473, T1454, T1455, T1441
        self.technique_id = insert_technique(self.attack_id, self.technique_name, self.technique_description)


class Subtechniques():

    def __init__(self, element, subtechnique_attack_id):
        super().__init__()
        self.attack_id = subtechnique_attack_id
        self.subtechnique_name = element['name']
        try:
            self.subtechnique_description = element['description']
        except KeyError:
            self.subtechnique_description = ''
        try:
            self.related_tactic = element['kill_chain_phases'][0]['phase_name']
        except KeyError:
            error.append(attack_id)
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

    return True # Change this in to something more meaningful


def insert_tactic(attack_id, tactic_name, tactic_description):

    existence = q.q_get_element_id.get_element_id('tactics', 'tactic_name', tactic_name)

    if existence is False:
        insert_into_table = q.q_insert_into_tables.insert_into_tables('tactics', attack_id, tactic_name, tactic_description)
        print('Created tactic %s' % tactic_name)
        return redirect(url_for('maps.completed'))
    else:
        return False


# Adding ATT&CK Techniques
def insert_technique(attack_id, technique_name, technique_description):

    insert_into_table = q.q_insert_into_tables.insert_into_tables('techniques', attack_id, technique_name, technique_description)

    print('Created technique %s' % technique_name)

    return insert_into_table


#REFACTOR THIS
def insert_subtechnique(attack_id, subtechnique_name, subtechnique_description):

    insert_into_table = q.q_insert_into_tables.insert_into_tables('subtechniques', attack_id, subtechnique_name, subtechnique_description)

    print('Created technique %s' % subtechnique_name)

    return insert_into_table


# Adding ATT&CK Adversaries
def insert_adversary(attack_id, adversary_name, adversary_description, attack_identifiers):

    insert_into_table = q.q_insert_adversary_into_tables.insert_adversary_into_tables('adversaries', adv.attack_id, adv.adversary_name, adv.adversary_description, adv.attack_identifiers)
    print('Created adversary %s' % adversary_name)
    return insert_into_table


# Adding ATT&CK Tools
def insert_tool(attack_id, tool_name, tool_description):

    insert_into_table = q.q_insert_into_tables.insert_into_tables('tools', attack_id, tool_name, tool_description)
    print('Created tool %s' % tool_name)
    return insert_into_table


# Insert Tools x Techniques ----- this is gatherin technique att&ck id, instead of technique id
def insert_toolxtec(tool_name, tool_id, techniques_used): 

    for element in techniques_used:

        technique_id = element['external_references'][0]['external_id']

        if '.' in technique_id:
            subtechnique_id = q.q_get_element_id.get_element_id('subtechniques', 'subtechnique_id', technique_id)
            result = q.q_insert_tool_x_techn.insert_tool_x_techn('tools_x_techniques', tool_id, subtechnique_id)
    
        else:
            q.q_get_element_id.get_element_id('techniques', 'technique_id', technique_id)
            result = q.q_insert_tool_x_techn.insert_tool_x_techn('tools_x_techniques', tool_id, technique_id)
        print('Created relationship for %s' % tool_name)
    return True


# Adding ATT&CK TacticxTechniques
def insert_tacxtec(technique_id, related_tactic):

    tactic = related_tactic.replace('-', ' ')
    tactic_id = q.q_get_element_id.get_element_id('tactics', 'tactic_name', tactic)
    try:
        tactic_x_technique = q.q_insert_tactic_x_technique.insert_tactic_x_technique(tactic_id, technique_id)
        print('Created tactic relationship')
    except KeyError:
        error.append(tactic_id)

    return redirect(url_for('maps.completed'))


# Insert relation insert_advxtool
def insert_advxtool(adversary_id, related_tools):
    
    for tool in tools_used:
        #check what tools_used brings
        tool_attack_id = q.q_get_element_id.get_element_id('tools', 'attack_id', tool_attack_id)

        result = q.q_insert_insert_adversary_x_tool.insert_insert_adversary_x_tool(adversary_id, tool_attack_id)
        print('Created adversary per tool relationship')    
    return True


# Insert Subtechniques x Techniques
def insert_tecxsubtec(related_technique, subattack_id):
    
    insert_into_table = q.q_insert_relation_into_tables.insert_relation_into_tables('techniques_x_subtechniques', 'technique_id', 'subtechnique_id', related_technique, subattack_id)
    print('Created technique per subtechnique relationship')
    return True
