from datetime import datetime
from app import db

class Maintenance(db.Model):
    __tablename__ = 'maintenance'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed, cancelled
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    due_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, title, description, equipment_id, user_id, due_date=None, priority='medium'):
        self.title = title
        self.description = description
        self.equipment_id = equipment_id
        self.user_id = user_id
        self.due_date = due_date
        self.priority = priority
        self.status = 'scheduled'
    
    def complete(self):
        """Mark maintenance task as completed"""
        self.status = 'completed'
        self.completed_date = datetime.utcnow()
    
    def start(self):
        """Mark maintenance task as in progress"""
        self.status = 'in_progress'
    
    def cancel(self):
        """Mark maintenance task as cancelled"""
        self.status = 'cancelled'
    
    def is_overdue(self):
        """Check if maintenance task is overdue"""
        if self.due_date and self.status != 'completed' and self.status != 'cancelled':
            return datetime.utcnow() > self.due_date
        return False
    
    def __repr__(self):
        return f'<Maintenance {self.title}>' 