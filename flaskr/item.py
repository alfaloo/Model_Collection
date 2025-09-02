from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dotenv import load_dotenv
from datetime import datetime
from flaskr.auth import login_required
from .models import User, Item, Comment, db
from .pagination_collection import PaginationCollection
load_dotenv()

bp = Blueprint('item', __name__)

@bp.route('/add_item', methods=('GET', 'POST'))
@login_required
def add_item():
    if request.method == 'POST':
        brand = request.form.get('brand', type=str)
        make = request.form.get('make', type=str)
        model = request.form.get('model', type=str)
        variant = request.form.get('variant', type=str)
        serial_number = request.form.get('serial_number', type=int) or None
        production_count = request.form.get('production_count', type=int) or None
        purchase_price = request.form.get('purchase_price', type=int)
        purchase_platform = request.form.get('purchase_platform', type=str)
        purchase_year = request.form.get('purchase_year', type=int)
        purchase_month = request.form.get('purchase_month', type=int)
        is_sold = bool(request.form.get('is_sold', type=bool))
        sold_price = request.form.get('sold_price', type=int) or None
        sold_platform = request.form.get('sold_platform', type=str) or None
        sold_year = request.form.get('sold_year', type=int) or None
        sold_month = request.form.get('sold_month', type=int) or None
        
        error = None
        if not brand:
            error = 'Brand is required.'
        elif not make:
            error = 'Make is required.'
        elif not model:
            error = 'Model is required.'
        elif not variant:
            error = 'Variant is required.'
        elif not purchase_price:
            error = 'Purchase price is required.'
        elif not purchase_platform:
            error = 'Purchase platform is required.'
        elif not purchase_year:
            error = 'Purchase year is required.'
        elif not purchase_month:
            error = 'Purchase month is required.'
        elif is_sold == None:
            error = 'Sale status is required.'
        
        if is_sold:
            if not sold_price:
                error = 'Sold price is required.'
            elif not sold_platform:
                error = 'Sold platform is required.'
            elif not sold_year:
                error = 'Sold year is required.'
            elif not sold_month:
                error = 'Sold month is required.'

        if error is not None:
            flash(error)
        else:
            new_item = Item(brand=brand,
                            make=make,
                            model=model,
                            variant=variant,
                            serial_number=serial_number,
                            production_count=production_count,
                            purchase_price=purchase_price,
                            purchase_platform=purchase_platform,
                            purchase_year=purchase_year,
                            purchase_month=purchase_month,
                            is_sold=is_sold,
                            sold_price=sold_price,
                            sold_platform=sold_platform,
                            sold_year=sold_year,
                            sold_month=sold_month)
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('main.index'))

    current_year = datetime.now().year + 1
    return render_template('item/add_item.html', current_year=current_year)

@bp.route('/update_item/<int:item_id>', methods=('GET', 'POST'))
@login_required
def update_item(item_id):
    if g.user.is_admin == 0:
        abort(403)

    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        brand = request.form.get('brand', type=str)
        make = request.form.get('make', type=str)
        model = request.form.get('model', type=str)
        variant = request.form.get('variant', type=str)
        serial_number = request.form.get('serial_number', type=int) or None
        production_count = request.form.get('production_count', type=int) or None
        purchase_price = request.form.get('purchase_price', type=int)
        purchase_platform = request.form.get('purchase_platform', type=str)
        purchase_year = request.form.get('purchase_year', type=int)
        purchase_month = request.form.get('purchase_month', type=int)
        is_sold = bool(request.form.get('is_sold', type=bool))
        sold_price = request.form.get('sold_price', type=int) or None
        sold_platform = request.form.get('sold_platform', type=str) or None
        sold_year = request.form.get('sold_year', type=int) or None
        sold_month = request.form.get('sold_month', type=int) or None

        error = None
        if not brand:
            error = 'Brand is required.'
        elif not make:
            error = 'Make is required.'
        elif not model:
            error = 'Model is required.'
        elif not variant:
            error = 'Variant is required.'
        elif not purchase_price:
            error = 'Purchase price is required.'
        elif not purchase_platform:
            error = 'Purchase platform is required.'
        elif not purchase_year:
            error = 'Purchase year is required.'
        elif not purchase_month:
            error = 'Purchase month is required.'
        elif is_sold == None:
            error = 'Sale status is required.'
        
        if is_sold:
            if not sold_price:
                error = 'Sold price is required.'
            elif not sold_platform:
                error = 'Sold platform is required.'
            elif not sold_year:
                error = 'Sold year is required.'
            elif not sold_month:
                error = 'Sold month is required.'

        if error is not None:
            flash(error)
        else:
            item.brand = brand
            item.make = make
            item.model = model
            item.variant = variant
            item.serial_number = serial_number
            item.production_count = production_count
            item.purchase_price = purchase_price
            item.purchase_platform = purchase_platform
            item.purchase_year = purchase_year
            item.purchase_month = purchase_month
            item.is_sold = is_sold
            item.sold_price = sold_price
            item.sold_platform = sold_platform
            item.sold_year = sold_year
            item.sold_month = sold_month

            db.session.commit()
            flash('Item is updated', 'success')
            return redirect(url_for('main.index'))

    current_year = datetime.now().year + 1
    return render_template('item/update_item.html', current_year=current_year, item=item)

@bp.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item_to_delete = Item.query.get_or_404(item_id)
    if item_to_delete:
        db.session.delete(item_to_delete)
        db.session.commit()
        flash(f"Item {item_id} deleted successfully", 'success')
    else:
        flash(f"Item with ID {item_id} not found", 'danger')
    return redirect(url_for('main.index'))

@bp.route('/view/<int:item_id>')
@login_required
def view_item(item_id):
    builder = (
        db.session.query(Comment, User)
        .filter(Comment.item_id == item_id)
        .join(User, Comment.author_id == User.id)
        .order_by(Comment.created.desc())
    )
    page = request.args.get('page', type=int, default=1)
    pagination_collection = PaginationCollection(builder, page)
    return render_template('item/view_item.html', item=Item.query.get_or_404(item_id), comment=pagination_collection.items, pagination=pagination_collection.pagination)
