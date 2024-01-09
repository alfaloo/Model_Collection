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
        'SELECT p.id, name, sex, date_of_birth, phone, address'
        ' FROM patient p'
        ' ORDER BY name ASC'
    ).fetchall()
    return render_template('blog/index.html', patients=patients)

@bp.route('/add_patient', methods=('GET', 'POST'))
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        address = request.form['address']
        error = None

        if not name:
            error = 'Name is required.'
        elif not date_of_birth:
            error = 'Date of Birth is required.'
        elif not phone:
            error = 'Phone is required.'
        elif not address:
            error = 'Address is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO patient (name, sex, date_of_birth, phone, address)'
                ' VALUES (?, ?, ?, ?, ?)',
                (str(name), str(sex), str(date_of_birth), str(phone), str(address))
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/add_patient.html')

@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        address = request.form['address']
        empty_search = True;

        query = 'SELECT * FROM patient p WHERE'
        if name:
            empty_search = False;
            query += f' name = "{name}" AND'
        if sex != "empty":
            empty_search = False;
            query += f' sex = "{sex}" AND'
        if date_of_birth:
            empty_search = False;
            query += f' date_of_birth = "{date_of_birth}" AND'
        if phone:
            empty_search = False;
            query += f' phone = "{phone}" AND'
        if address:
            empty_search = False;
            query += f' address = "{address}" AND'

        query = query[:-3]

        db = get_db()
        if empty_search:
            patients = db.execute(
                'SELECT p.id, name, sex, date_of_birth, phone, address'
                ' FROM patient p'
                ' ORDER BY name ASC'
            ).fetchall()
        else:
            query += 'ORDER BY name DESC;'
            patients = db.execute(query).fetchall()

        return render_template('blog/index.html', patients=patients)

    return render_template('blog/search.html')

def get_patient(patient_id):
    patient = get_db().execute(
        'SELECT p.id, name, sex, date_of_birth, phone, address'
        ' FROM patient p'
        ' WHERE p.id = ?',
        (patient_id,)
    ).fetchone()

    if patient is None:
        abort(404, f"Patient id {patient_id} doesn't exist.")

    return patient

@bp.route('/update_patient/<int:patient_id>', methods=('GET', 'POST'))
@login_required
def update_patient(patient_id):
    if  g.user['is_admin'] == 0:
        abort(403)

    patient = get_patient(patient_id)

    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        address = request.form['address']
        error = None

        if not name:
            error = 'Name is required.'
        elif not date_of_birth:
            error = 'Date of Birth is required.'
        elif not phone:
            error = 'Phone is required.'
        elif not address:
            error = 'Address is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE patient SET name = ?, sex = ?, date_of_birth = ?, phone = ?, address = ?'
                ' WHERE id = ?',
                (str(name), str(sex), str(date_of_birth), str(phone), str(address), patient_id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update_patient.html', patient=patient)

@bp.route('/delte_patient/<int:patient_id>', methods=('POST',))
@login_required
def delete_patient(patient_id):
    get_patient(patient_id)
    db = get_db()
    db.execute('DELETE FROM patient WHERE id = ?', (patient_id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/add_diagnosis/<int:patient_id>', methods=('GET', 'POST'))
@login_required
def add_diagnosis(patient_id):
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        error = None

        if not category:
            error = 'Category is required.'
        elif not description:
            error = 'Description of Birth is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO diagnosis (category, description, author_id, patient_id)'
                ' VALUES (?, ?, ?, ?)',
                (str(category), str(description), g.user['id'], patient_id)
            )
            db.commit()
            return redirect(url_for('blog.view_patient', patient_id=patient_id))

    return render_template('blog/add_diagnosis.html', patient_id=patient_id)

def get_diagnosis(diagnosis_id, check_author=True):
    diagnosis = get_db().execute(
        'SELECT d.id, category, description, created, author_id, patient_id'
        ' FROM diagnosis d JOIN user u ON d.author_id = u.id'
        ' WHERE d.id = ?',
        (diagnosis_id,)
    ).fetchone()

    if diagnosis is None:
        abort(404, f"Patient id {diagnosis_id} doesn't exist.")

    if check_author and diagnosis['author_id'] != g.user['id']:
        abort(403)

    return diagnosis

@bp.route('/update_diagnosis/<int:diagnosis_id>', methods=('GET', 'POST'))
@login_required
def update_diagnosis(diagnosis_id):
    diagnosis = get_diagnosis(diagnosis_id)

    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        error = None

        if not category:
            error = 'Category is required.'
        elif not description:
            error = 'Description of Birth is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE diagnosis SET category = ?, description = ?'
                ' WHERE id = ?',
                (str(category), str(description), diagnosis_id)
            )
            db.commit()
            return redirect(url_for('blog.view_patient', patient_id=diagnosis['patient_id']))

    return render_template('blog/update_diagnosis.html', diagnosis=diagnosis)

@bp.route('/view/<int:patient_id>')
@login_required
def view_patient(patient_id):
    db = get_db()
    query = f'SELECT d.id, category, description, created, author_id, patient_id, username FROM diagnosis d JOIN user u ON d.author_id = u.id WHERE d.patient_id = {patient_id} ORDER BY created DESC'
    diagnosis = db.execute(query).fetchall()
    return render_template('blog/view_patient.html', patient=get_patient(patient_id), diagnosis=diagnosis)

@bp.route('/delete_diagnosis/<int:diagnosis_id>', methods=('POST',))
@login_required
def delete_diagnosis(diagnosis_id):
    get_diagnosis(diagnosis_id)
    db = get_db()
    db.execute('DELETE FROM diagnosis WHERE id = ?', (diagnosis_id,))
    db.commit()
    return redirect(url_for('blog.index'))