# Adding ATT&CK Adversaries
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


    # ATT&CK FRAMEWORK INTERACTION 
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
                create_subtechnique(technique_id, technique_name, technique_description)
            else:
                insert_into_table = q.q_insert_into_tables.insert_into_tables('techniques', technique_id, technique_name, technique_description)
                print('Created technique %s' % technique_name)
        except KeyError:
            error.append(technique_id)
            # MOBILE TECHNIQUES MISSING TACTIC REFERENCE:
            #T1443, T1425, T1442, T1419, T1440, T1462, T1460, T1459, T1457, T1445, T1431, T1434, T1473, T1454, T1455, T1441

            print(error)

    return redirect(url_for('maps.completed'))


def create_subtechnique(technique_id, subtechnique_name, subtechnique_description):

    subtechnique_attack_id = ''
    technique_attack_id = ''

    if '.' in technique_id: 
        technique_attack_id,subtechnique_attack_id = technique_id.split('.', 1)
        related_technique=q.q_get_element_id.get_element_id('techniques', 'technique_id', technique_attack_id)

    insert_into_table = q.q_insert_into_tables.insert_into_tables('subtechniques', subtechnique_attack_id, subtechnique_name, subtechnique_description)
    subtechnique_id=q.q_get_element_id.get_element_id('subtechniques', 'subtechnique_id', subtechnique_attack_id)

    techniques_x_subtechniques(related_technique, subtechnique_id)

    return redirect(url_for('maps.completed'))


# Adding ATT&CK Adversaries
def get_groups():
    lift = attack_client()
    groups = lift.get_groups()

    for element in groups:
        

        insert_into_table = q.q_insert_adversary_into_tables.insert_adversary_into_tables('adversaries', group_id, group_name, group_description, group_identifiers)

    return redirect(url_for('maps.completed'))


# Adding ATT&CK Tools
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


# Adding ATT&CK TacticxTechniques
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


# Insert Subtechniques x Techniques
def techniques_x_subtechniques(related_technique, subtechnique_id):
    
    insert_into_table = q.q_insert_relation_into_tables.insert_relation_into_tables('techniques_x_subtechniques', 'technique_id', 'subtechnique_id', related_technique, subtechnique_id)

    return True


# Insert Tools x Techniques
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
