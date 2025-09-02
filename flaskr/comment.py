from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dotenv import load_dotenv

from flaskr.auth import login_required
from .models import Comment, db
load_dotenv()

bp = Blueprint('comment', __name__)

@bp.route('/add_comment/<int:item_id>', methods=('GET', 'POST'))
@login_required
def add_comment(item_id):
    if request.method == 'POST':
        category = request.form.get('category', type=str)
        description = request.form.get('description', type=str) or None
        
        error = None
        if not category:
            error = 'Category is required.'
        elif not description:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            new_comment = Comment(
                category=category,
                description=description,
                author_id=g.user.id,
                item_id=item_id
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('item.view_item', item_id=item_id))

    return render_template('comment/add_comment.html', item_id=item_id)

@bp.route('/update_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def update_comment(comment_id):
    comment = get_comment(comment_id)

    if request.method == 'POST':
        category = request.form.get('category', type=str)
        description = request.form.get('description', type=str) or None

        error = None
        if not category:
            error = 'Category is required.'
        elif not description:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            Comment.query.filter_by(id=comment_id).update(
                {"category": category, "description": description}
            )
            db.session.commit()
            return redirect(url_for('item.view_item', item_id=comment.item_id))

    return render_template('comment/update_comment.html', comment=comment)

@bp.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    item_id = get_comment(comment_id).item_id
    comment_to_delete = Comment.query.get(comment_id)

    if comment_to_delete:
        db.session.delete(comment_to_delete)
        db.session.commit()
        flash(f"Comment deleted successfully", 'success')
    else:
        flash(f"Comment not found", 'danger')

    return redirect(url_for('item.view_item', item_id=item_id))

def get_comment(comment_id, check_author=True):
    comment = Comment.query.get(comment_id)

    if comment is None:
        abort(404, f"Item id {comment_id} doesn't exist.")

    if check_author and comment.author_id != g.user.id:
        abort(403)

    return comment