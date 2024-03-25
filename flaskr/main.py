from flask import (
    Blueprint, render_template, request
)
from dotenv import load_dotenv

from flaskr.auth import login_required
from .models import Patient
from .pagination_collection import PaginationCollection
load_dotenv()

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    builder = Patient.query.order_by(Patient.name)
    page = request.args.get('page', type=int, default=1)

    pagination_collection = PaginationCollection(builder, page)

    return render_template('main/index.html', patients=pagination_collection.items, pagination=pagination_collection.pagination, endpoint='main.index')

@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    if not request.args:
        return render_template('main/search.html', patients={}, pagination=None)
    name = request.args.get('name', type=str, default=None)
    sex = request.args.get('sex', type=str, default=None)
    date_of_birth = request.args.get('date_of_birth', type=str, default=None)
    phone = request.args.get('phone', type=str, default=None)
    address = request.args.get('address', type=str, default=None)

    builder = Patient.query.order_by(Patient.name)

    if name:
        builder = builder.filter_by(name=name)
        print('yes')
    if sex:
        builder = builder.filter_by(sex=sex)
    if date_of_birth:
        builder = builder.filter_by(date_of_birth=date_of_birth)
    if phone:
        builder = builder.filter_by(phone=phone)
    if address:
        builder = builder.filter_by(address=address)

    page = request.args.get('page', type=int, default=1)

    pagination_collection = PaginationCollection(builder, page)
    return render_template('main/search.html', patients=pagination_collection.items, pagination=pagination_collection.pagination)
