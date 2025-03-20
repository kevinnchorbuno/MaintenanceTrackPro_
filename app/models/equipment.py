import random
from datetime import datetime
import os
import qrcode
from io import BytesIO
from PIL import Image
from app import db

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    qr_code_path = db.Column(db.String(255))
    health_score = db.Column(db.Float, default=lambda: random.uniform(60, 100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    maintenance_logs = db.relationship('Maintenance', backref='equipment', lazy='dynamic')
    added_by = db.relationship('User', foreign_keys=[user_id], backref=db.backref('added_equipment', lazy='dynamic'))
    
    def __init__(self, name, description, user_id, image_path=None):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.image_path = image_path
        self.health_score = random.uniform(60, 100)
        self.generate_qr_code()
    
    def generate_qr_code(self):
        """Generate QR code for equipment and save it"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'/equipment/view/{self.id}')
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        qr_code_dir = os.path.join('app', 'static', 'images', 'qrcodes')
        os.makedirs(qr_code_dir, exist_ok=True)
        
        file_name = f'qr_equipment_{self.id}.png'
        file_path = os.path.join(qr_code_dir, file_name)
        
        img.save(file_path)
        self.qr_code_path = f'images/qrcodes/{file_name}'
    
    def update_health_score(self, new_score=None):
        """Update health score manually or generate random"""
        if new_score and 0 <= new_score <= 100:
            self.health_score = new_score
        else:
            self.health_score = random.uniform(60, 100)
    
    def get_health_status(self):
        """Return health status based on health score"""
        if self.health_score >= 70:
            return 'healthy'
        elif self.health_score >= 60:
            return 'warning'
        else:
            return 'critical'
    
    def __repr__(self):
        return f'<Equipment {self.name}>' 