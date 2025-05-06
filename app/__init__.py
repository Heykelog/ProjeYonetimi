import os
import logging
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure database
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_development')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///pentest.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    
    # E-posta konfigürasyonu
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@pentestapp.com')
    app.config['ADMIN_EMAIL'] = os.environ.get('ADMIN_EMAIL', 'admin@pentestapp.com')
    app.config['APP_URL'] = os.environ.get('APP_URL', 'http://localhost:5001')
    
    # Initialize extensions
    db.init_app(app)
    Bootstrap(app)
    
    # Import models
    from app.models import Company, Project, Finding
    
    # Register blueprints
    from app.views.company import company_bp
    from app.views.project import project_bp
    from app.views.finding import finding_bp
    from app.views.report import report_bp
    from app.views.main import main_bp
    from app.views.setting import setting_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(company_bp, url_prefix='/companies')
    app.register_blueprint(project_bp, url_prefix='/projects')
    app.register_blueprint(finding_bp, url_prefix='/findings')
    app.register_blueprint(report_bp, url_prefix='/reports')
    app.register_blueprint(setting_bp, url_prefix='/settings')
    
    # Register CLI commands
    from app import commands
    commands.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Add template context processors
    @app.context_processor
    def inject_now():
        return {'current_year': datetime.utcnow().year}
    
    # Log all requests
    @app.before_request
    def log_request_info():
        app.logger.debug('Headers: %s', request.headers)
        app.logger.debug('Body: %s', request.get_data())

    @app.errorhandler(500)
    def handle_500(error):
        app.logger.error('Server Error: %s', error)
        return 'Internal Server Error', 500
    
    return app 