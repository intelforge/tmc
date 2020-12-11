from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts

# Get list of all adversaries per tool available in the database.
def get_adversaries_x_tool():

    db = get_db()
    try:
        db.row_factory = make_dicts
        query = db.execute(
            "SELECT a.adversary_id As \'Adversary ID\', a.adversary_name as Adversary, t.tool_id as \'Tool ID\', t.tool_name as Tool \
                FROM adversaries a \
                inner join adversaries_x_tools axt on axt.adversary_id=a.id \
                inner join tools t on axt.tool_id=t.id \
                ORDER BY a.adversary_name").fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 