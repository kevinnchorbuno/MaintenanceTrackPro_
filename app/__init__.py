import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config=None):
    app = Flask(__name__)
    
    # Configure the app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///maintenancetrackpro.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Apply custom configurations if provided
    if config:
        app.config.update(config)
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.equipment import equipment_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.maintenance import maintenance_bp
    from app.routes.reports import reports_bp
    from app.routes.profile import profile_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(profile_bp)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Jinja2 template filters
    @app.template_filter('tojson')
    def to_json(value):
        import json
        return json.dumps(value)
    
    return app 