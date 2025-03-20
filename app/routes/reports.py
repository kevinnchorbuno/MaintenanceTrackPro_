from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta

from app import db
from app.models.equipment import Equipment
from app.models.maintenance import Maintenance
from app.models.user import User

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/')
@login_required
def index():
    """Reports dashboard"""
    if not current_user.is_admin() and not current_user.is_boss():
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
    cancelled_tasks = Maintenance.query.filter_by(status='cancelled').count()
    
    # Get user statistics
    total_users = User.query.count()
    boss_count = User.query.filter_by(role='boss').count()
    admin_count = User.query.filter_by(role='admin').count()
    engineer_count = User.query.filter_by(role='engineer').count()
    
    # Generate time-based data
    # For demo purposes, we'll create synthetic data
    # In a real application, you'd query this from your database with appropriate date filtering
    dates = []
    maintenance_counts = []
    today = datetime.now()
    
    for i in range(30):
        date = today - timedelta(days=29-i)
        dates.append(date.strftime('%Y-%m-%d'))
        # Generate random data between 1-10
        import random
        maintenance_counts.append(random.randint(1, 10))
    
    return render_template(
        'reports/index.html',
        title='Reports Dashboard',
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
            'scheduled': scheduled_tasks,
            'cancelled': cancelled_tasks
        },
        user_stats={
            'total': total_users,
            'boss': boss_count,
            'admin': admin_count,
            'engineer': engineer_count
        },
        time_series_data={
            'dates': dates,
            'maintenance_counts': maintenance_counts
        }
    )

@reports_bp.route('/equipment-health')
@login_required
def equipment_health():
    """Detailed equipment health report"""
    if not current_user.is_admin() and not current_user.is_boss():
        return redirect(url_for('dashboard.index'))
    
    # Get all equipment
    equipment_list = Equipment.query.all()
    
    return render_template(
        'reports/equipment_health.html',
        title='Equipment Health Report',
        equipment_list=equipment_list
    )

@reports_bp.route('/maintenance-efficiency')
@login_required
def maintenance_efficiency():
    """Maintenance efficiency report"""
    if not current_user.is_admin() and not current_user.is_boss():
        return redirect(url_for('dashboard.index'))
    
    # Get completed maintenance tasks
    completed_tasks = Maintenance.query.filter_by(status='completed').all()
    
    # Calculate efficiency metrics
    # For demo purposes, we'll create synthetic data
    # In a real application, you'd calculate actual metrics based on due dates vs completed dates
    metrics = {
        'on_time': 75,  # Percentage of tasks completed on time
        'average_completion_days': 3.2,  # Average days to complete a task
        'overdue_rate': 15,  # Percentage of tasks that were overdue when completed
    }
    
    return render_template(
        'reports/maintenance_efficiency.html',
        title='Maintenance Efficiency Report',
        completed_tasks=completed_tasks,
        metrics=metrics
    )

@reports_bp.route('/generate-pdf/<report_type>')
@login_required
def generate_pdf(report_type):
    """Generate PDF report (placeholder for future implementation)"""
    if not current_user.is_admin() and not current_user.is_boss():
        return redirect(url_for('dashboard.index'))
    
    # This would be implemented with a PDF generation library like WeasyPrint or ReportLab
    # For now, we'll just redirect back with a message
    
    from flask import flash
    flash('PDF generation will be implemented in a future version.', 'info')
    
    if report_type == 'equipment':
        return redirect(url_for('reports.equipment_health'))
    elif report_type == 'maintenance':
        return redirect(url_for('reports.maintenance_efficiency'))
    else:
        return redirect(url_for('reports.index')) 