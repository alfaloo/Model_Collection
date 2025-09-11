from flask import (
    Blueprint, render_template, request
)
from dotenv import load_dotenv
from datetime import datetime

from flaskr.auth import login_required
from .models import Item
from .pagination_collection import PaginationCollection
load_dotenv()

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    builder = Item.query.order_by(Item.brand)
    page = request.args.get('page', type=int, default=1)

    pagination_collection = PaginationCollection(builder, page)

    return render_template('main/index.html', items=pagination_collection.items, pagination=pagination_collection.pagination, endpoint='main.index')

@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    current_year = datetime.now().year + 1

    if not request.args:
        return render_template('main/search.html', current_year=current_year, items={}, pagination=None)
    
    brand = request.args.get('brand', type=str) or None
    make = request.args.get('make', type=str) or None
    model = request.args.get('model', type=str) or None
    variant = request.args.get('variant', type=str) or None
    scale = request.args.get('scale', type=str) or None
    serial_number = request.args.get('serial_number', type=int) or None
    production_count = request.args.get('production_count', type=int) or None
    grade = request.args.get('grade', type=str) or None
    purchase_price = request.args.get('purchase_price', type=int) or None
    purchase_platform = request.args.get('purchase_platform', type=str) or None
    purchase_year = request.args.get('purchase_year', type=int) or None
    purchase_month = request.args.get('purchase_month', type=int) or None
    is_sold = request.args.get('is_sold', type=str) or None
    sold_price = request.args.get('sold_price', type=int) or None
    sold_platform = request.args.get('sold_platform', type=str) or None
    sold_year = request.args.get('sold_year', type=int) or None
    sold_month = request.args.get('sold_month', type=int) or None

    if is_sold == 'True':
        is_sold = True
    elif is_sold == 'False':
        is_sold = False

    builder = Item.query.order_by(Item.brand)
    print(grade)
    if brand:
        builder = builder.filter(Item.brand.ilike(f"%{brand}%"))
    if make:
        builder = builder.filter(Item.make.ilike(f"%{make}%"))
    if model:
        builder = builder.filter(Item.model.ilike(f"%{model}%"))
    if variant:
        builder = builder.filter(Item.variant.ilike(f"%{variant}%"))
    if scale:
        builder = builder.filter(Item.scale.ilike(f"%{scale}%"))
    if serial_number:
        builder = builder.filter_by(serial_number=serial_number)
    if production_count:
        builder = builder.filter_by(production_count=production_count)
    if grade:
        if grade == 'None':
            builder = builder.filter(Item.grade.is_(None))
        else:
            builder = builder.filter_by(grade=int(grade))
    if purchase_price:
        builder = builder.filter_by(purchase_price=purchase_price)
    if purchase_platform:
        builder = builder.filter_by(purchase_platform=purchase_platform)
    if purchase_year:
        builder = builder.filter_by(purchase_year=purchase_year)
    if purchase_month:
        builder = builder.filter_by(purchase_month=purchase_month)
    if is_sold != None:
        builder = builder.filter_by(is_sold=is_sold)
    if sold_price:
        builder = builder.filter_by(sold_price=sold_price)
    if sold_platform:
        builder = builder.filter_by(sold_platform=sold_platform)
    if sold_year:
        builder = builder.filter_by(sold_year=sold_year)
    if sold_month:
        builder = builder.filter_by(sold_month=sold_month)

    page = request.args.get('page', type=int, default=1)

    pagination_collection = PaginationCollection(builder, page)
    return render_template('main/search.html', current_year=current_year, items=pagination_collection.items, pagination=pagination_collection.pagination)
