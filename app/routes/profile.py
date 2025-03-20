from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash

from app import db
from app.models.user import User
from app.models.maintenance import Maintenance
from app.forms.auth_forms import ChangePasswordForm

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
@login_required
def view():
    """View user profile"""
    # Get recent maintenance tasks assigned to the user
    recent_tasks = Maintenance.query.filter_by(user_id=current_user.id).order_by(Maintenance.created_at.desc()).limit(5).all()
    
    # Get completed task count
    completed_tasks_count = Maintenance.query.filter_by(user_id=current_user.id, status='completed').count()
    
    # Get total assigned task count
    total_tasks_count = Maintenance.query.filter_by(user_id=current_user.id).count()
    
    # Calculate completion rate
    completion_rate = (completed_tasks_count / total_tasks_count * 100) if total_tasks_count > 0 else 0
    
    return render_template(
        'profile/view.html',
        title='My Profile',
        recent_tasks=recent_tasks,
        completed_tasks_count=completed_tasks_count,
        total_tasks_count=total_tasks_count,
        completion_rate=completion_rate
    )

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Edit user profile"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        # Check if username or email already exists (excluding current user)
        if username != current_user.username and User.query.filter_by(username=username).first():
            flash('Username already taken. Please try another.', 'danger')
            return redirect(url_for('profile.edit'))
        
        if email != current_user.email and User.query.filter_by(email=email).first():
            flash('Email already registered. Please try another.', 'danger')
            return redirect(url_for('profile.edit'))
        
        # Update user
        current_user.username = username
        current_user.email = email
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.view'))
    
    return render_template(
        'profile/edit.html',
        title='Edit Profile'
    )

@profile_bp.route('/password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('profile.change_password'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('profile.view'))
    
    return render_template(
        'profile/change_password.html',
        title='Change Password',
        form=form
    ) 