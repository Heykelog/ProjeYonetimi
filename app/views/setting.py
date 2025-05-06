from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models.setting import Setting
from app.forms.setting import SettingsForm
import os

setting_bp = Blueprint('setting', __name__)

@setting_bp.route('/', methods=['GET', 'POST'])
def index():
    form = SettingsForm()
    
    # If form is submitted and validated
    if form.validate_on_submit():
        # Save SMTP settings
        Setting.set_setting('MAIL_SERVER', form.mail_server.data)
        Setting.set_setting('MAIL_PORT', str(form.mail_port.data))
        Setting.set_setting('MAIL_USE_TLS', '1' if form.mail_use_tls.data else '0')
        Setting.set_setting('MAIL_USE_SSL', '1' if form.mail_use_ssl.data else '0')
        Setting.set_setting('MAIL_USERNAME', form.mail_username.data)
        # Only update password if provided
        if form.mail_password.data:
            Setting.set_setting('MAIL_PASSWORD', form.mail_password.data)
        Setting.set_setting('MAIL_DEFAULT_SENDER', form.mail_default_sender.data)
        Setting.set_setting('ADMIN_EMAIL', form.admin_email.data)
        
        # Save application settings
        Setting.set_setting('APP_URL', form.app_url.data)
        Setting.set_setting('REMINDER_SEND_TIME', form.reminder_send_time.data)
        
        flash('Ayarlar başarıyla kaydedildi!', 'success')
        return redirect(url_for('setting.index'))
    
    # Pre-populate form with existing settings
    else:
        form.mail_server.data = Setting.get_setting('MAIL_SERVER', os.environ.get('MAIL_SERVER', 'smtp.gmail.com'))
        form.mail_port.data = int(Setting.get_setting('MAIL_PORT', os.environ.get('MAIL_PORT', '587')))
        form.mail_use_tls.data = Setting.get_setting('MAIL_USE_TLS', '1') == '1'
        form.mail_use_ssl.data = Setting.get_setting('MAIL_USE_SSL', '0') == '1'
        form.mail_username.data = Setting.get_setting('MAIL_USERNAME', os.environ.get('MAIL_USERNAME', ''))
        form.mail_default_sender.data = Setting.get_setting('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@pentestapp.com'))
        form.admin_email.data = Setting.get_setting('ADMIN_EMAIL', os.environ.get('ADMIN_EMAIL', 'admin@pentestapp.com'))
        form.app_url.data = Setting.get_setting('APP_URL', os.environ.get('APP_URL', 'http://localhost:5001'))
        form.reminder_send_time.data = Setting.get_setting('REMINDER_SEND_TIME', '09:00')
    
    return render_template('setting/index.html', form=form)

def get_smtp_settings():
    """Helper function to get SMTP settings for the email util"""
    return {
        'MAIL_SERVER': Setting.get_setting('MAIL_SERVER', os.environ.get('MAIL_SERVER', 'smtp.gmail.com')),
        'MAIL_PORT': int(Setting.get_setting('MAIL_PORT', os.environ.get('MAIL_PORT', '587'))),
        'MAIL_USE_TLS': Setting.get_setting('MAIL_USE_TLS', '1') == '1',
        'MAIL_USE_SSL': Setting.get_setting('MAIL_USE_SSL', '0') == '1',
        'MAIL_USERNAME': Setting.get_setting('MAIL_USERNAME', os.environ.get('MAIL_USERNAME', '')),
        'MAIL_PASSWORD': Setting.get_setting('MAIL_PASSWORD', os.environ.get('MAIL_PASSWORD', '')),
        'MAIL_DEFAULT_SENDER': Setting.get_setting('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@pentestapp.com')),
        'ADMIN_EMAIL': Setting.get_setting('ADMIN_EMAIL', os.environ.get('ADMIN_EMAIL', 'admin@pentestapp.com')),
        'APP_URL': Setting.get_setting('APP_URL', os.environ.get('APP_URL', 'http://localhost:5001')),
    } 