from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    patients = db.execute(
        'SELECT p.id, name, sex, age, description, created, author_id, username'
        ' FROM patient p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', patients=patients)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        age = request.form['age']
        description = request.form['description']
        error = None

        if not name:
            error = 'Name is required.'
        elif not age:
            error = 'Age is required.'
        elif not description:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO patient (name, sex, age, description, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (str(name), str(sex), str(age), str(description), g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    if request.method == 'POST':
        criteria_1 = request.form['criteria_1']
        criteria_1_value = request.form['criteria_1_value']
        double_criteria = False
        criteria_2 = None
        criteria_2_value = None

        if request.form['criteria_2_value'] != "":
            double_criteria = True
            criteria_2 = request.form['criteria_2']
            criteria_2_value = request.form['criteria_2_value']

        db = get_db()
        query = f'SELECT * FROM patient WHERE {criteria_1} = "{criteria_1_value}"'
        if double_criteria:
            query += f' AND {criteria_2} = "{criteria_2_value}"'
        query += ' ORDER BY created DESC;'
        patients = db.execute(query).fetchall()
        return render_template('blog/index.html', patients=patients)

    return render_template('blog/search.html')

def get_patient(id, check_author=True):
    patient = get_db().execute(
        'SELECT p.id, name, sex, age, description, created, author_id, username'
        ' FROM patient p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if patient is None:
        abort(404, f"Patient id {id} doesn't exist.")

    if check_author and patient['author_id'] != g.user['id']:
        abort(403)

    return patient

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    patients = get_patient(id)

    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        age = request.form['age']
        description = request.form['description']
        error = None

        if not name:
            error = 'Name is required.'
        elif not age:
            error = 'Age is required.'
        elif not description:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE patient SET name = ?, sex = ?, age = ?, description = ?'
                ' WHERE id = ?',
                (name, sex, age, description, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', patients=patients)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_patient(id)
    db = get_db()
    db.execute('DELETE FROM patient WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))