from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dotenv import load_dotenv

from flaskr.auth import login_required
from .models import Diagnosis, db
load_dotenv()

bp = Blueprint('diagnosis', __name__)

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
            return redirect(url_for('patient.view_patient', patient_id=patient_id))

    return render_template('diagnosis/add_diagnosis.html', patient_id=patient_id)

@bp.route('/update_diagnosis/<int:diagnosis_id>', methods=['GET', 'POST'])
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
            Diagnosis.query.filter_by(id=diagnosis_id).update(
                {"category": category, "description": description}
            )
            db.session.commit()
            return redirect(url_for('patient.view_patient', patient_id=diagnosis.patient_id))

    return render_template('diagnosis/update_diagnosis.html', diagnosis=diagnosis)

@bp.route('/delete_diagnosis/<int:diagnosis_id>', methods=['POST'])
@login_required
def delete_diagnosis(diagnosis_id):
    patient_id = get_diagnosis(diagnosis_id).patient_id
    diagnosis_to_delete = Diagnosis.query.get(diagnosis_id)

    if diagnosis_to_delete:
        db.session.delete(diagnosis_to_delete)
        db.session.commit()
        flash(f"Diagnosis deleted successfully", 'success')
    else:
        flash(f"Diagnosis not found", 'danger')

    return redirect(url_for('patient.view_patient', patient_id=patient_id))

def get_diagnosis(diagnosis_id, check_author=True):
    diagnosis = Diagnosis.query.get(diagnosis_id)

    if diagnosis is None:
        abort(404, f"Patient id {diagnosis_id} doesn't exist.")

    if check_author and diagnosis.author_id != g.user.id:
        abort(403)

    return diagnosis