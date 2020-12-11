from flask import ( g )
from tmc.db import get_db, make_dicts

# Get list of adversary techniques available in the database.
def get_tools_techniques(tool_id):

    db = get_db()
    db.row_factory = make_dicts
    try:
        query = db.execute('select t.tool_name as Tool, tec.technique_id as \'Technique ID\', \
            tec.technique_name as Technique,  null as \'Subtechnique I\', null as Subtechnique \
            From tools t \
            inner join tools_x_techniques tt on t.id = tt.tool_id \
            inner join techniques tec on tec.id = tt.technique_id \
            where t.id=? \
            UNION ALL \
            select t.tool_name  as Tool , tec.technique_id, tec.technique_name,  stec.subtechnique_id \
            , stec.subtechnique_name from tools t \
            inner join tools_x_subtechniques st on t.id = st.tool_id \
            inner join techniques_x_subtechniques ts on st.subtechnique_id=ts.subtechnique_id \
            inner join techniques tec on tec.id=ts.technique_id \
            inner join subtechniques stec on stec.id = st.subtechnique_id \
            where t.id=? \
            ORDER BY t.tool_name, tec.technique_id, stec.subtechnique_id'
            (tool_id, tool_id, ))
        result = query.fetchall()
        return result
    except TypeError:
        return False