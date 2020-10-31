from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts
from attackcti import attack_client
from IPython import embed

# Get list of all tools per technique available in the database.
def get_tools_x_techniques():

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            'SELECT t.tool_id As \'Tool ID\', t.tool_name as Tool, tec.technique_id as \'Technique ID\', tec.technique_name as Technique \
                FROM tools t \
                inner join adversaries_x_tools axt on axt.tool_id=t.id \
                inner join tools_x_techniques txt on txt.technique_id=t.id \
                inner join techniques tec on tec.id=txt.technique_id \
                ORDER BY t.tool_name').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 