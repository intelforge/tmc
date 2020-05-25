from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from tmc.auth import login_required
from tmc.db import get_db
from attackcti import attack_client
from IPython import embed

bp = Blueprint('maps', __name__)

#NOT IN USE, SEARCH FOR HOME - the Select here is not useful
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, adversary_name, adversary_description, created, author_id, username'
        ' FROM adversaries p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('maps/index.html', posts=posts)


# Creates the new adversary in the database
@bp.route('/create-adversary', methods=('GET', 'POST'))
@login_required
def create_adversary():
    if request.method == 'POST':
        adversary_name = request.form['name']
        adversary_description = request.form['description']
        error = None

        if not adversary_name:
            error = 'Adversary name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO adversaries (adversary_name, adversary_description, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('maps.create_adversary'))

    return render_template('maps/create-adversary.html')


# Creates the new tool in the database
@bp.route('/create-tool', methods=('GET', 'POST'))
@login_required
def create_tool():
    if request.method == 'POST':
        tool_name = request.form['name']
        tool_description = request.form['description']
        error = None

        if not tool_name:
            error = 'Tool name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tools (tool_name, tool_description, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('maps.create_tool'))

    return render_template('maps/create-tool.html')


# Creates the new technique in the database
@bp.route('/create-technique', methods=('GET', 'POST'))
@login_required
def create_technique():
    if request.method == 'POST':
        tool_name = request.form['name']
        tool_description = request.form['description']
        error = None

        if not tool_name:
            error = 'Technique name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO techniques (technique_name, technique_description, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('maps.create_technique'))

    return render_template('maps/create-technique.html')


# Creates the new subtechnique in the database
@bp.route('/create-subtechnique', methods=('GET', 'POST'))
@login_required
def create_subtechnique():
    if request.method == 'POST':
        tool_name = request.form['name']
        tool_description = request.form['description']
        error = None

        if not tool_name:
            error = 'Subtechnique name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO subtechniques (subtechnique_name, subtechnique_description, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('maps.create_subtechnique'))

    return render_template('maps/create-subtechnique.html')


# This function is not in use
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


# Function to update db, needs fixing
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('maps.index'))

    return render_template('maps/update.html', post=post)


# Function to delete entry from the database, needs fixing
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('maps.index'))


# Functions to extract information with attackcti
@bp.route('/attackcti_techniques', methods=('GET', 'POST'))
@login_required
def get_techniques():
    lift = attack_client()
    enterprise_techniques = lift.get_enterprise_techniques()

    for element in enterprise_techniques:
        technique_name = element['external_references'][0]['external_id'] + ' — ' + element['name']
        technique_description = element['description']
        technique_tactic = element['kill_chain_phases'][0]['phase_name'] 
        # MAKE INSERT FUNCTION FOR THE DATABASE

    return techniques


@bp.route('/attackcti_tactics', methods=('GET', 'POST'))
@login_required
def get_tactics():
    lift = attack_client()
    enterprise_tactics = lift.get_enterprise_tactics()

    for element in enterprise_tactics:
        tactic_name = element['external_references'][0]['external_id'] + ' — ' + element['name']
        tactic_description = element['description']
        # MAKE INSERT FUNCTION FOR THE DATABASE

    return tactics


@bp.route('/attackcti_groups', methods=('GET', 'POST'))
@login_required
def get_groups():
    lift = attack_client()
    enterprise_groups = lift.get_enterprise_groups()

    for element in enterprise_groups:
        group_name = element['name']
        group_description = element['description']
        group_aliases = element['aliases']
        # MAKE INSERT FUNCTION FOR THE DATABASE

    return groups


@bp.route('/attackcti_tools', methods=('GET', 'POST'))
@login_required
def get_tools():
    lift = attack_client()
    enterprise_tools = lift.get_enterprise_tools()

    for element in enterprise_tools:
        tool_name = element['name']
        tool_description = element['description']
        tool_aliases = element['x_mitre_aliases']
        # MAKE INSERT FUNCTION FOR THE DATABASE

    return tools
