from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

from app import db
from app.models.equipment import Equipment
from app.models.maintenance import Maintenance
from app.models.notification import Notification
from app.models.user import User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """Redirect to appropriate dashboard based on user role"""
    if current_user.is_boss():
        return redirect(url_for('dashboard.boss'))
    elif current_user.is_admin():
        return redirect(url_for('dashboard.admin'))
    else:
        return redirect(url_for('dashboard.engineer'))

@dashboard_bp.route('/boss')
@login_required
def boss():
    """Boss dashboard with equipment overview and team performance"""
    if not current_user.is_boss():
        return redirect(url_for('dashboard.index'))
    
    # Get equipment statistics
    total_equipment = Equipment.query.count()
    healthy_count = Equipment.query.filter(Equipment.health_score >= 70).count()
    warning_count = Equipment.query.filter(Equipment.health_score >= 60, Equipment.health_score < 70).count()
    critical_count = Equipment.query.filter(Equipment.health_score < 60).count()
    
    # Calculate percentages
    healthy_percent = (healthy_count / total_equipment * 100) if total_equipment > 0 else 0
    warning_percent = (warning_count / total_equipment * 100) if total_equipment > 0 else 0
    critical_percent = (critical_count / total_equipment * 100) if total_equipment > 0 else 0
    
    # Get maintenance statistics
    total_maintenance = Maintenance.query.count()
    completed_tasks = Maintenance.query.filter_by(status='completed').count()
    in_progress_tasks = Maintenance.query.filter_by(status='in_progress').count()
    scheduled_tasks = Maintenance.query.filter_by(status='scheduled').count()
    
    # Get user statistics
    total_users = User.query.count()
    boss_count = User.query.filter_by(role='boss').count()
    admin_count = User.query.filter_by(role='admin').count()
    engineer_count = User.query.filter_by(role='engineer').count()
    
    # Get recent notifications
    notifications = Notification.query.order_by(Notification.created_at.desc()).limit(5).all()
    
    return render_template(
        'dashboard/boss.html',
        title='Boss Dashboard',
        equipment_stats={
            'total': total_equipment,
            'healthy': healthy_count,
            'warning': warning_count,
            'critical': critical_count,
            'healthy_percent': healthy_percent,
            'warning_percent': warning_percent,
            'critical_percent': critical_percent
        },
        maintenance_stats={
            'total': total_maintenance,
            'completed': completed_tasks,
            'in_progress': in_progress_tasks,
            'scheduled': scheduled_tasks
        },
        user_stats={
            'total': total_users,
            'boss': boss_count,
            'admin': admin_count,
            'engineer': engineer_count
        },
        notifications=notifications
    )

@dashboard_bp.route('/admin')
@login_required
def admin():
    """Admin dashboard with user management focus"""
    if not current_user.is_admin() and not current_user.is_boss():
        return redirect(url_for('dashboard.index'))
    
    # Get all users for management
    users = User.query.all()
    
    # Count users by role
    boss_count = User.query.filter_by(role='boss').count()
    admin_count = User.query.filter_by(role='admin').count()
    engineer_count = User.query.filter_by(role='engineer').count()
    
    # Get recent notifications
    notifications = Notification.query.order_by(Notification.created_at.desc()).limit(5).all()
    
    return render_template(
        'dashboard/admin.html',
        title='Admin Dashboard',
        users=users,
        user_stats={
            'total': len(users),
            'boss': boss_count,
            'admin': admin_count,
            'engineer': engineer_count
        },
        notifications=notifications
    )

@dashboard_bp.route('/engineer')
@login_required
def engineer():
    """Engineer dashboard with equipment health and maintenance focus"""
    # Get equipment list
    equipment_list = Equipment.query.all()
    
    # Get maintenance tasks - show all tasks, not just assigned to current user
    maintenance_tasks = Maintenance.query.filter(
        (Maintenance.status == 'scheduled') | (Maintenance.status == 'in_progress')
    ).order_by(Maintenance.due_date).limit(10).all()
    
    # Get notifications
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(5).all()
    
    # Get selected equipment (first one by default)
    selected_equipment = None
    if equipment_list:
        selected_equipment = equipment_list[0]
    
    return render_template(
        'dashboard/engineer.html',
        title='Engineer Dashboard',
        equipment_list=equipment_list,
        selected_equipment=selected_equipment,
        maintenance_tasks=maintenance_tasks,
        notifications=notifications
    )

@dashboard_bp.route('/notifications')
@login_required
def notifications():
    """View all notifications"""
    # Get all notifications for the user based on role
    if current_user.is_boss() or current_user.is_admin():
        # Admins and bosses see all notifications
        notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    else:
        # Engineers see their notifications
        notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    
    return render_template(
        'dashboard/notifications.html',
        title='All Notifications',
        notifications=notifications
    ) 