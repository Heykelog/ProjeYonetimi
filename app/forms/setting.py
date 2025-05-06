from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, NumberRange

class SettingsForm(FlaskForm):
    # SMTP Settings
    mail_server = StringField('SMTP Sunucusu', validators=[DataRequired()])
    mail_port = IntegerField('SMTP Port', validators=[DataRequired(), NumberRange(min=1, max=65535)])
    mail_use_tls = BooleanField('TLS Kullan')
    mail_use_ssl = BooleanField('SSL Kullan')
    mail_username = StringField('SMTP Kullanıcı Adı', validators=[Optional()])
    mail_password = PasswordField('SMTP Şifresi', validators=[Optional()])
    mail_default_sender = StringField('Varsayılan Gönderici', validators=[DataRequired(), Email()])
    admin_email = StringField('Yönetici E-posta', validators=[DataRequired(), Email()])
    
    # App Settings
    app_url = StringField('Uygulama URL', validators=[DataRequired()])
    reminder_send_time = StringField('Hatırlatma Gönderim Saati (HH:MM)', validators=[DataRequired()])
    
    submit = SubmitField('Ayarları Kaydet') 