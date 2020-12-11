from flask import ( g )
from tmc.db import get_db, make_dicts
from IPython import embed

# Get list of all adversaries available in the database.
def get_adversaries(adversary=''):

    db = get_db()
    db.row_factory = make_dicts
    try:
        if not adversary:
            query = db.execute('SELECT id as db_id, adversary_id as ID, adversary_name as Adversary, adversary_identifiers as Identifiers, adversary_description as Description \
                FROM adversaries ORDER BY adversary_name ASC').fetchall()
            return query
        else:
            query = db.execute(
                'SELECT * FROM adversaries WHERE id is ?',
            (adversary,)
            ).fetchone()
            return query
    except TypeError:
        return False