from flask import ( g )
from tmc.db import get_db, make_dicts

# Get list of adversary techniques available in the database.
def get_adversaries_techniques(adversary_id):

    db = get_db()
    db.row_factory = make_dicts
    try:
        query = db.execute('select t.tool_name as Tool, tec.technique_id as TechniqueID, \
            tec.technique_name as Technique,  null as SubtechniqueID, null as Subtechnique \
            from adversaries_x_tools at \
            inner join tools t on at.tool_id = t.id \
            inner join tools_x_techniques tt on t.id = tt.tool_id \
            inner join techniques tec on tec.id = tt.technique_id \
            where at.adversary_id=? \
            \
            UNION ALL\
            \
            select t.tool_name  as Tool , tec.technique_id, tec.technique_name,  stec.subtechnique_id \
            , stec.subtechnique_name from adversaries_x_tools at  \
            inner join tools t on at.tool_id = t.id \
            inner join tools_x_subtechniques st on t.id = st.tool_id \
            inner join techniques_x_subtechniques ts on st.subtechnique_id=ts.subtechnique_id \
            inner join techniques tec on tec.id=ts.technique_id \
            inner join subtechniques stec on stec.id = st.subtechnique_id \
            where at.adversary_id=? \
            ORDER BY t.tool_name, tec.technique_id, stec.subtechnique_id' ,
            (adversary_id, adversary_id, ))
        result = query.fetchall()
        return result
    except TypeError:
        return False