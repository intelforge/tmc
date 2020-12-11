from flask import ( g, redirect, url_for )
from tmc.db import get_db, make_dicts

# Get list of all events per industry available in the database.
def get_events_x_industry():

    db = get_db()
    db.row_factory = make_dicts
    try:
        query = db.execute(
            'select a.adversary_name, i.industry_name, e.event_name from events e \
            inner join events_x_industries ei on e.id = ei.event_id \
            inner join industries i on i.id = ei.industry_id \
            inner join adversaries_x_events ae on ae.event_id = e.id \
            inner join adversaries a on a.id = ae.adversary_id').fetchall()
        return query
    except TypeError:
        #embed()
        return False #Change this for something more meaningful -- warning/alert 