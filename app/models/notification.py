from datetime import datetime
from app import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='info')  # info, warning, critical
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)
    
    def __init__(self, title, message, user_id, equipment_id=None, type='info'):
        self.title = title
        self.message = message
        self.user_id = user_id
        self.equipment_id = equipment_id
        self.type = type
        self.is_read = False
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
    
    def mark_as_unread(self):
        """Mark notification as unread"""
        self.is_read = False
    
    @staticmethod
    def create_equipment_notification(equipment, user_id, message_type='info'):
        """Create notification for equipment"""
        if message_type == 'warning':
            title = f'Warning: {equipment.name} health declining'
            message = f'The health score of {equipment.name} has dropped to {equipment.health_score:.1f}%.'
        elif message_type == 'critical':
            title = f'CRITICAL: {equipment.name} requires attention'
            message = f'The health score of {equipment.name} has dropped to a critical level of {equipment.health_score:.1f}%!'
        else:
            title = f'Info: {equipment.name} status update'
            message = f'The health score of {equipment.name} is currently {equipment.health_score:.1f}%.'
        
        notification = Notification(
            title=title,
            message=message,
            user_id=user_id,
            equipment_id=equipment.id,
            type=message_type
        )
        return notification
    
    @staticmethod
    def create_maintenance_notification(maintenance, user_id):
        """Create notification for maintenance"""
        from app.models.equipment import Equipment
        
        # Get equipment
        equipment = Equipment.query.get(maintenance.equipment_id)
        equipment_name = equipment.name if equipment else "Unknown Equipment"
        
        if maintenance.status == 'completed':
            title = f'Maintenance Completed: {maintenance.title}'
            message = f'The maintenance task for {equipment_name} has been completed.'
            type = 'info'
        elif maintenance.is_overdue():
            title = f'Overdue Maintenance: {maintenance.title}'
            message = f'The maintenance task for {equipment_name} is overdue.'
            type = 'warning'
        else:
            title = f'Scheduled Maintenance: {maintenance.title}'
            message = f'A new maintenance task has been scheduled for {equipment_name}.'
            type = 'info'
        
        notification = Notification(
            title=title,
            message=message,
            user_id=user_id,
            equipment_id=maintenance.equipment_id,
            type=type
        )
        return notification
    
    def __repr__(self):
        return f'<Notification {self.title}>' 