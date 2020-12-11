from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts

# Get list of all tools per technique available in the database.
def get_tools_x_subtechniques(subtechnique=''):

    db = get_db()
    db.row_factory = make_dicts
    try:
        if subtechnique:
            query = db.execute(
                'SELECT t.tool_id As \'ToolID\', t.tool_name as Tool, subtec.subtechnique_id as \'SubtechniqueID\', subtec.subtechnique_name as Subtechnique \
                    FROM tools t \
                    inner join adversaries_x_tools axt on axt.tool_id=t.id \
                    inner join tools_x_subtechniques txt on txt.subtechnique_id=t.id \
                    inner join subtechniques subtec on subtec.id=txt.subtechnique_id \
                    WHERE t.id=?', (subtechnique, )).fetchall()
            return query
        else:
            query = db.execute(
                'SELECT t.tool_id As \'ToolID\', t.tool_name as Tool, subtec.subtechnique_id as \'SubtechniqueID\', subtec.subtechnique_name as Subtechnique \
                    FROM tools t \
                    inner join adversaries_x_tools axt on axt.tool_id=t.id \
                    inner join tools_x_subtechniques txt on txt.subtechnique_id=t.id \
                    inner join subtechniques subtec on subtec.id=txt.subtechnique_id \
                    ORDER BY t.tool_name').fetchall()
            return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 