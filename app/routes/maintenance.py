from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime

from app import db
from app.models.maintenance import Maintenance
from app.models.equipment import Equipment
from app.models.notification import Notification
from app.forms.maintenance_forms import MaintenanceForm

maintenance_bp = Blueprint('maintenance', __name__, url_prefix='/maintenance')

@maintenance_bp.route('/')
@login_required
def index():
    """List all maintenance tasks"""
    # Different views based on user role
    if current_user.is_boss() or current_user.is_admin():
        # Admins and bosses see all tasks
        maintenance_tasks = Maintenance.query.order_by(Maintenance.due_date).all()
    else:
        # Engineers see all tasks for better coordination
        maintenance_tasks = Maintenance.query.order_by(Maintenance.due_date).all()
    
    # Group tasks by status
    scheduled = [t for t in maintenance_tasks if t.status == 'scheduled']
    in_progress = [t for t in maintenance_tasks if t.status == 'in_progress']
    completed = [t for t in maintenance_tasks if t.status == 'completed']
    
    return render_template(
        'maintenance/index.html',
        title='Maintenance Tasks',
        scheduled_tasks=scheduled,
        in_progress_tasks=in_progress,
        completed_tasks=completed
    )

@maintenance_bp.route('/add/<int:equipment_id>', methods=['GET', 'POST'])
@login_required
def add(equipment_id):
    """Add new maintenance task for specific equipment"""
    equipment = Equipment.query.get_or_404(equipment_id)
    form = MaintenanceForm()
    
    if form.validate_on_submit():
        maintenance = Maintenance(
            title=form.title.data,
            description=form.description.data,
            equipment_id=equipment.id,
            user_id=current_user.id,
            due_date=form.due_date.data,
            priority=form.priority.data,
        )
        
        db.session.add(maintenance)
        
        # Create notification for the maintenance task
        notification = Notification.create_maintenance_notification(maintenance, current_user.id)
        db.session.add(notification)
        
        db.session.commit()
        flash('Maintenance task added successfully!', 'success')
        return redirect(url_for('equipment.view', id=equipment.id))
    
    return render_template(
        'maintenance/add.html',
        title='Add Maintenance Task',
        form=form,
        equipment=equipment
    )

@maintenance_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit existing maintenance task"""
    maintenance = Maintenance.query.get_or_404(id)
    
    # All engineers can edit any maintenance task
    if not current_user.is_boss() and not current_user.is_admin() and not current_user.role == 'engineer':
        flash('You are not authorized to edit this maintenance task.', 'danger')
        return redirect(url_for('maintenance.index'))
    
    form = MaintenanceForm()
    
    if form.validate_on_submit():
        # If status is changing to completed, set completed date
        old_status = maintenance.status
        new_status = form.status.data
        
        maintenance.title = form.title.data
        maintenance.description = form.description.data
        maintenance.priority = form.priority.data
        maintenance.due_date = form.due_date.data
        maintenance.status = new_status
        
        # If status is being set to completed now, update completed date
        if old_status != 'completed' and new_status == 'completed':
            maintenance.completed_date = datetime.utcnow()
            
            # Assign to current user if completing and not already assigned
            if not maintenance.user_id:
                maintenance.user_id = current_user.id
                
            # Create notification for completion
            notification = Notification.create_maintenance_notification(maintenance, current_user.id)
            db.session.add(notification)
        
        db.session.commit()
        flash('Maintenance task updated successfully!', 'success')
        return redirect(url_for('maintenance.view', id=maintenance.id))
    elif request.method == 'GET':
        form.title.data = maintenance.title
        form.description.data = maintenance.description
        form.priority.data = maintenance.priority
        form.due_date.data = maintenance.due_date
        form.status.data = maintenance.status
    
    return render_template(
        'maintenance/edit.html',
        title='Edit Maintenance Task',
        form=form,
        maintenance=maintenance
    )

@maintenance_bp.route('/view/<int:id>')
@login_required
def view(id):
    """View maintenance task details"""
    maintenance = Maintenance.query.get_or_404(id)
    
    return render_template(
        'maintenance/view.html',
        title=f'Maintenance: {maintenance.title}',
        maintenance=maintenance
    )

@maintenance_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    """Delete maintenance task"""
    maintenance = Maintenance.query.get_or_404(id)
    
    # Any engineer can delete maintenance tasks
    if not current_user.is_boss() and not current_user.is_admin() and not current_user.role == 'engineer':
        flash('You are not authorized to delete this maintenance task.', 'danger')
        return redirect(url_for('maintenance.index'))
    
    equipment_id = maintenance.equipment_id
    
    # Delete related notifications
    Notification.query.filter_by(equipment_id=equipment_id, title=f'Scheduled Maintenance: {maintenance.title}').delete()
    
    # Delete the maintenance task
    db.session.delete(maintenance)
    db.session.commit()
    
    flash('Maintenance task has been deleted.', 'success')
    return redirect(url_for('equipment.view', id=equipment_id))

@maintenance_bp.route('/change-status/<int:id>/<string:status>')
@login_required
def change_status(id, status):
    """Quick route to change maintenance status"""
    maintenance = Maintenance.query.get_or_404(id)
    
    # Engineers can change status of any maintenance task
    if not current_user.is_boss() and not current_user.is_admin() and not current_user.role == 'engineer':
        flash('You are not authorized to change this maintenance task.', 'danger')
        return redirect(url_for('maintenance.index'))
    
    old_status = maintenance.status
    
    if status == 'start':
        maintenance.start()
        # Assign to current user if starting and not already assigned
        if not maintenance.user_id:
            maintenance.user_id = current_user.id
        flash('Maintenance task marked as in progress.', 'info')
    elif status == 'complete':
        maintenance.complete()
        # Assign to current user if completing and not already assigned
        if not maintenance.user_id:
            maintenance.user_id = current_user.id
        flash('Maintenance task marked as completed.', 'success')
        
        # Create notification for completion
        if old_status != 'completed':
            notification = Notification.create_maintenance_notification(maintenance, current_user.id)
            db.session.add(notification)
    elif status == 'cancel':
        maintenance.cancel()
        flash('Maintenance task cancelled.', 'warning')
    
    db.session.commit()
    return redirect(request.referrer or url_for('maintenance.view', id=maintenance.id)) 