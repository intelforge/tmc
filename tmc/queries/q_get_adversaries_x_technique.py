from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all adversaries per technique available in the database.
def get_adversaries_x_technique():

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            'SELECT a.adversary_id As \'Adversary ID\', a.adversary_name as Adversary,  t.technique_id as \'Technique ID\', t.technique_name as Technique, s.subtechnique_id as \'Subtechnique ID\',s.subtechnique_name as Subtechnique \
                FROM adversaries a \
                inner join adversaries_x_tools axt on axt.adversary_id=a.id \
                inner join tools_x_techniques txt on txt.tool_id=axt.tool_id \
                inner join techniques t on t.id=txt.technique_id \
                ORDER BY a.adversary_name').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 