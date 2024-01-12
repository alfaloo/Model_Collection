from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_paginate import Pagination, get_page_parameter
from werkzeug.exceptions import abort
from dotenv import load_dotenv
import os

from flaskr.auth import login_required
from .models import User, Patient, Diagnosis, db
from .pagination_collection import PaginationCollection
load_dotenv()

bp = Blueprint('blog', __name__)

@bp.route('/')
@login_required
def index():
    builder = Patient.query.order_by(Patient.name)
    page = request.args.get('page', type=int, default=1)

    pagination_collection = PaginationCollection(builder, page)

    return render_template('blog/index.html', patients=pagination_collection.items, pagination=pagination_collection.pagination, endpoint='blog.index')

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
            new_patient = Patient(name=str(name), sex=str(sex), date_of_birth=str(date_of_birth), phone=str(phone), address=str(address))
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/add_patient.html')

@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    name = request.args.get('name', type=str, default=None)
    sex = request.args.get('sex', type=str, default=None)
    date_of_birth = request.args.get('date_of_birth', type=str, default=None)
    phone = request.args.get('phone', type=str, default=None)
    address = request.args.get('address', type=str, default=None)

    builder = Patient.query.order_by(Patient.name)

    if name:
        builder = builder.filter_by(name=name)
        print('yes')
    if sex != "":
        builder = builder.filter_by(sex=sex)
    if date_of_birth:
        builder = builder.filter_by(date_of_birth=date_of_birth)
    if phone:
        builder = builder.filter_by(phone=phone)
    if address:
        builder = builder.filter_by(address=address)

    page = request.args.get('page', type=int, default=1)

    pagination_collection = PaginationCollection(builder, page)

    return render_template('blog/search.html', patients=pagination_collection.items, pagination=pagination_collection.pagination)

def get_patient(patient_id):
    patient = Patient.query.get(patient_id)

    if patient is None:
        abort(404, f"Patient id {patient_id} doesn't exist.")

    return patient

@bp.route('/update_patient/<int:patient_id>', methods=('GET', 'POST'))
@login_required
def update_patient(patient_id):
    if g.user.is_admin == 0:
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
            Patient.query.filter_by(id=patient_id).update(
                {"name": name, "sex": sex, "date_of_birth": date_of_birth, "phone": phone, "address": address}
            )
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update_patient.html', patient=patient)


@bp.route('/delete_patient/<int:patient_id>', methods=('POST',))
@login_required
def delete_patient(patient_id):
    patient_to_delete = Patient.query.get(patient_id)
    if patient_to_delete:
        db.session.delete(patient_to_delete)
        db.session.commit()
        flash(f"Patient {patient_id} deleted successfully", 'success')
    else:
        flash(f"Patient with ID {patient_id} not found", 'danger')
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
            new_diagnosis = Diagnosis(
                category=category,
                description=description,
                author_id=g.user.id,
                patient_id=patient_id
            )
            db.session.add(new_diagnosis)
            db.session.commit()
            return redirect(url_for('blog.view_patient', patient_id=patient_id))

    return render_template('blog/add_diagnosis.html', patient_id=patient_id)


def get_diagnosis(diagnosis_id, check_author=True):
    diagnosis = Diagnosis.query.get(diagnosis_id)

    if diagnosis is None:
        abort(404, f"Patient id {diagnosis_id} doesn't exist.")

    if check_author and diagnosis.author_id != g.user.id:
        abort(403)

    return diagnosis


@bp.route('/update_diagnosis/<int:diagnosis_id>', methods=('GET', 'PUT'))
@login_required
def update_diagnosis(diagnosis_id):
    diagnosis = get_diagnosis(diagnosis_id)

    if request.method == 'PUT':
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
            Diagnosis.query.filter_by(id=diagnosis_id).update(
                {"category": category, "description": description}
            )
            db.session.commit()
            return redirect(url_for('blog.view_patient', patient_id=diagnosis.patient_id))

    return render_template('blog/update_diagnosis.html', diagnosis=diagnosis)


@bp.route('/view/<int:patient_id>')
@login_required
def view_patient(patient_id):
    builder = (
        Diagnosis.query.join(User)
        .filter(Diagnosis.patient_id == patient_id)
        .order_by(Diagnosis.created.desc())
    )
    page = request.args.get('page', type=int, default=1)
    pagination_collection = PaginationCollection(builder, page)
    return render_template('blog/view_patient.html', patient=get_patient(patient_id), diagnosis=pagination_collection.items, pagination=pagination_collection.pagination)


@bp.route('/delete_diagnosis/<int:diagnosis_id>', methods=('POST',))
@login_required
def delete_diagnosis(diagnosis_id):
    patient_id = get_diagnosis(diagnosis_id).patient_id
    diagnosis_to_delete = Diagnosis.query.get(diagnosis_id)

    if diagnosis_to_delete:
        db.session.delete(diagnosis_to_delete)
        db.session.commit()
        flash(f"Diagnosis {diagnosis_id} deleted successfully", 'success')
    else:
        flash(f"Diagnosis {diagnosis_id} not found", 'danger')

    return redirect(url_for('blog.view_patient', patient_id=patient_id))
