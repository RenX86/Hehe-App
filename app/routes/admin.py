from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.user import User
from app import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users', methods=['GET'])
@login_required
def manage_users():
    # Check if current user is admin (you can add an is_admin column to User model if needed)
    if not current_user.is_approved:  # For now, only approved users can manage others
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/approve/<int:user_id>', methods=['POST'])
@login_required
def approve_user(user_id):
    if not current_user.is_approved:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash(f'User {user.username} has been approved.', 'success')
    return redirect(url_for('admin.manage_users'))

@bp.route('/disapprove/<int:user_id>', methods=['POST'])
@login_required
def disapprove_user(user_id):
    if not current_user.is_approved:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    user.is_approved = False
    db.session.commit()
    flash(f'User {user.username} has been disapproved.', 'success')
    return redirect(url_for('admin.manage_users')) 