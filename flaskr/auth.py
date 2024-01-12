import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from .pagination_collection import PaginationCollection

from .models import User, Patient, Diagnosis, db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/users', methods=('GET', 'POST'))
def users():
    if not g.user.is_admin:
        abort(403)

    builder = User.query.order_by(User.username)

    page = request.args.get('page', type=int, default=1)

    pagination_collection = PaginationCollection(builder, page)

    return render_template('auth/users/index.html', pagination_collection=pagination_collection)

@bp.route('/users/<int:id>', methods=('GET', 'POST'))
def user_edit(id):

    if not g.user.is_admin:
        abort(403)

    user = User.query.get_or_404(id)

    if request.method == 'POST':
        username = request.form.get('username', type=str)
        password = request.form.get('password', type=str, default=None)
        confirm_password = request.form.get('confirmation', type=str, default=None)
        is_admin = request.form.get('is_admin', type=bool, default=False)
        if password:
            if password != confirm_password:
                error = 'Passwords do not match.'
            else:
                user.password = generate_password_hash(password)

        user.username = username
        user.is_admin = is_admin
        db.session.commit()
        if 'error' in locals():
            flash(error)
        else:
            flash('User is updated', 'success')
            return redirect(url_for('auth.users'))

    return render_template('auth/users/form.html', user=user)
@bp.route('/users/create', methods=('GET', 'POST'))
def user_create():
    if not g.user.is_admin:
        abort(403)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        is_admin = request.form.get('is_admin')

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirmation:
            error = 'Passwords do not match.'
        elif User.query.filter_by(username=username).count():
            error = f"User {username} is already registered."

        if 'error' in locals():
            flash(error)
        else:
            new_user = User(username=username, password=generate_password_hash(password), is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.users"))

    return render_template('auth/users/form.html', user=User())


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        error = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = User.query.get(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
