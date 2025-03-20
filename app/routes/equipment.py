import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import random
import uuid
from PIL import Image
import qrcode
from io import BytesIO

from app import db
from app.models.equipment import Equipment
from app.models.maintenance import Maintenance
from app.models.notification import Notification
from app.forms.equipment_forms import EquipmentForm, EquipmentSearchForm

equipment_bp = Blueprint('equipment', __name__, url_prefix='/equipment')

def save_equipment_image(form_image):
    """Save equipment image and return the path"""
    # Generate a unique filename
    random_hex = uuid.uuid4().hex
    _, file_extension = os.path.splitext(form_image.filename)
    filename = random_hex + file_extension
    
    # Create directory if it doesn't exist
    upload_dir = os.path.join('app', 'static', 'images', 'equipment')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save the image
    file_path = os.path.join(upload_dir, filename)
    
    # Resize image to save space
    image = Image.open(form_image)
    image.thumbnail((800, 800))
    image.save(file_path)
    
    # Return the relative path for storage in db
    return f'images/equipment/{filename}'

@equipment_bp.route('/')
@login_required
def index():
    """List all equipment"""
    search_form = EquipmentSearchForm()
    search_term = request.args.get('search', '')
    
    if search_term:
        equipment_list = Equipment.query.filter(Equipment.name.ilike(f'%{search_term}%')).all()
    else:
        equipment_list = Equipment.query.all()
    
    return render_template(
        'equipment/index.html',
        title='Equipment List',
        equipment_list=equipment_list,
        search_form=search_form,
        search_term=search_term
    )

@equipment_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new equipment"""
    form = EquipmentForm()
    
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            image_path = save_equipment_image(form.image.data)
        
        equipment = Equipment(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id,
            image_path=image_path
        )
        
        if form.health_score.data:
            equipment.health_score = form.health_score.data
        
        db.session.add(equipment)
        db.session.commit()
        
        # After commit, generate QR code (needs equipment.id)
        equipment.generate_qr_code()
        db.session.commit()
        
        flash('Equipment added successfully!', 'success')
        return redirect(url_for('equipment.view', id=equipment.id))
    
    return render_template('equipment/add.html', title='Add Equipment', form=form)

@equipment_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit existing equipment"""
    equipment = Equipment.query.get_or_404(id)
    form = EquipmentForm()
    
    if form.validate_on_submit():
        equipment.name = form.name.data
        equipment.description = form.description.data
        
        if form.image.data:
            equipment.image_path = save_equipment_image(form.image.data)
        
        if form.health_score.data:
            equipment.health_score = form.health_score.data
        
        db.session.commit()
        flash('Equipment updated successfully!', 'success')
        return redirect(url_for('equipment.view', id=equipment.id))
    elif request.method == 'GET':
        form.name.data = equipment.name
        form.description.data = equipment.description
        form.health_score.data = equipment.health_score
    
    return render_template('equipment/edit.html', title='Edit Equipment', form=form, equipment=equipment)

@equipment_bp.route('/view/<int:id>')
@login_required
def view(id):
    """View equipment details"""
    equipment = Equipment.query.get_or_404(id)
    maintenance_history = Maintenance.query.filter_by(equipment_id=equipment.id).order_by(Maintenance.created_at.desc()).all()
    
    return render_template(
        'equipment/view.html',
        title=f'Equipment: {equipment.name}',
        equipment=equipment,
        maintenance_history=maintenance_history
    )

@equipment_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    """Delete equipment"""
    equipment = Equipment.query.get_or_404(id)
    
    # Check if user is admin or boss
    if not current_user.is_admin() and not current_user.is_boss():
        flash('You do not have permission to delete equipment.', 'danger')
        return redirect(url_for('equipment.index'))
    
    equipment_name = equipment.name
    
    # Delete related maintenance tasks
    Maintenance.query.filter_by(equipment_id=equipment.id).delete()
    
    # Delete related notifications
    Notification.query.filter_by(equipment_id=equipment.id).delete()
    
    # Delete the equipment
    db.session.delete(equipment)
    db.session.commit()
    
    flash(f'Equipment "{equipment_name}" has been deleted.', 'success')
    return redirect(url_for('equipment.index'))

@equipment_bp.route('/update-health/<int:id>')
@login_required
def update_health(id):
    """Update equipment health score (random for simulation)"""
    equipment = Equipment.query.get_or_404(id)
    
    old_health_status = equipment.get_health_status()
    equipment.update_health_score()
    new_health_status = equipment.get_health_status()
    
    # Create notification if health status changes to worse
    if (old_health_status == 'healthy' and new_health_status != 'healthy') or \
       (old_health_status == 'warning' and new_health_status == 'critical'):
        notification = Notification.create_equipment_notification(
            equipment, 
            current_user.id,
            'warning' if new_health_status == 'warning' else 'critical'
        )
        db.session.add(notification)
    
    db.session.commit()
    flash(f'Health score for {equipment.name} updated to {equipment.health_score:.1f}%', 'info')
    
    return redirect(url_for('equipment.view', id=equipment.id))

@equipment_bp.route('/scanner')
@login_required
def scanner():
    """QR code scanner page"""
    return render_template(
        'equipment/scanner.html',
        title='QR Code Scanner'
    )

@equipment_bp.route('/history/<int:id>')
@login_required
def history(id):
    """Show equipment health history"""
    equipment = Equipment.query.get_or_404(id)
    
    # In a real app, you would fetch historical data from a table
    # For now, we'll generate fake history data
    import random
    from datetime import datetime, timedelta
    
    # Generate 30 days of history data
    dates = []
    scores = []
    current_date = datetime.now()
    
    for i in range(30):
        date = current_date - timedelta(days=i)
        dates.insert(0, date.strftime('%Y-%m-%d'))
        
        # Generate a score close to the current score but with some variation
        base_score = equipment.health_score
        variation = random.uniform(-5, 5)
        score = max(min(base_score + variation, 100), 50)  # Keep between 50-100
        scores.insert(0, round(score, 1))
    
    history_data = {
        'dates': dates,
        'scores': scores
    }
    
    return render_template(
        'equipment/history.html',
        title=f'{equipment.name} History',
        equipment=equipment,
        history_data=history_data
    )

@equipment_bp.route('/regenerate-qrcodes')
@login_required
def regenerate_qrcodes():
    """Regenerate QR codes for all equipment"""
    if not current_user.is_admin() and not current_user.is_boss():
        flash('You do not have permission to regenerate QR codes.', 'danger')
        return redirect(url_for('equipment.index'))
    
    equipment_list = Equipment.query.all()
    for equipment in equipment_list:
        equipment.generate_qr_code()
    
    db.session.commit()
    flash(f'QR codes have been regenerated for {len(equipment_list)} equipment items.', 'success')
    return redirect(url_for('equipment.index')) 