import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from app.models.project import Project
from flask import current_app
import os

def send_email(subject, recipients, body, sender=None):
    """
    Send an email with the given subject and body to the specified recipients.
    
    Args:
        subject (str): Email subject
        recipients (list): List of recipient email addresses
        body (str): Email body content (HTML)
        sender (str, optional): Sender email address. Defaults to MAIL_DEFAULT_SENDER from config.
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Import here to avoid circular imports
        from app.views.setting import get_smtp_settings
        
        # Get email configuration from database settings or app config as fallback
        settings = get_smtp_settings()
        smtp_server = settings.get('MAIL_SERVER')
        smtp_port = settings.get('MAIL_PORT')
        smtp_username = settings.get('MAIL_USERNAME')
        smtp_password = settings.get('MAIL_PASSWORD')
        default_sender = settings.get('MAIL_DEFAULT_SENDER')
        use_tls = settings.get('MAIL_USE_TLS')
        use_ssl = settings.get('MAIL_USE_SSL')
        
        # If no sender is provided, use the default
        if not sender:
            sender = default_sender
            
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        
        # Attach HTML body
        html_part = MIMEText(body, 'html')
        msg.attach(html_part)
        
        # Send email with TLS or SSL based on settings
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            if use_tls:
                server.starttls()
                
        if smtp_username and smtp_password:
            server.login(smtp_username, smtp_password)
            
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()
        
        current_app.logger.info(f"Email sent: {subject} to {recipients}")
        return True
    
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False

def send_project_reminder_email(project, recipients=None):
    """
    Send a reminder email for a project with an upcoming pentest date.
    
    Args:
        project (Project): The project to send reminder for
        recipients (list, optional): List of email recipients. If None, will use default recipients.
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    if not recipients:
        admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@pentestapp.com')
        recipients = [admin_email]
    
    # Format the pentest date
    pentest_date = project.pentest_date.strftime("%d.%m.%Y")
    
    subject = f"HATIRLATMA: Pentest Tarihi Yaklaşıyor - {project.name}"
    
    # HTML Body with some styling
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ width: 100%; max-width: 600px; margin: 0 auto; }}
            .header {{ background-color: #007bff; color: white; padding: 15px; text-align: center; }}
            .content {{ padding: 20px; }}
            .footer {{ text-align: center; font-size: 12px; color: #777; padding: 10px; }}
            .highlight {{ color: #dc3545; font-weight: bold; }}
            .info-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 15px; }}
            .info-table th, .info-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            .info-table th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Pentest Tarihi Hatırlatması</h2>
            </div>
            <div class="content">
                <p>Sayın Yetkili,</p>
                
                <p>Aşağıdaki projenin pentest tarihi yaklaşmaktadır:</p>
                
                <table class="info-table">
                    <tr>
                        <th>Proje Adı:</th>
                        <td>{project.name}</td>
                    </tr>
                    <tr>
                        <th>Şirket:</th>
                        <td>{project.company.name}</td>
                    </tr>
                    <tr>
                        <th>Proje Yöneticisi:</th>
                        <td>{project.manager}</td>
                    </tr>
                    <tr>
                        <th>Pentest Tarihi:</th>
                        <td class="highlight">{pentest_date}</td>
                    </tr>
                    <tr>
                        <th>Adam-Gün:</th>
                        <td>{project.mandays}</td>
                    </tr>
                    <tr>
                        <th>Proje Türü:</th>
                        <td>{"Proje" if project.project_type == "Proje" else "Küçük Talep"}</td>
                    </tr>
                </table>
                
                <p>Lütfen gerekli hazırlıkları yapınız ve ilgili ekipleri bilgilendiriniz.</p>
                
                <p>Proje detaylarını görüntülemek için <a href="{current_app.config.get('APP_URL', 'http://localhost:5001')}/project/{project.id}">buraya tıklayınız</a>.</p>
                
                <p>Saygılarımızla,<br>Pentest Yönetim Sistemi</p>
            </div>
            <div class="footer">
                <p>Bu e-posta otomatik olarak gönderilmiştir. Lütfen yanıtlamayınız.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(subject, recipients, body)

def check_upcoming_pentests():
    """
    Check for projects with pentest dates approaching (tomorrow) and send reminder emails.
    This function should be called daily by a scheduler.
    
    Returns:
        int: Number of reminders sent
    """
    # Get projects with pentest date tomorrow
    tomorrow = datetime.now().date() + timedelta(days=1)
    upcoming_projects = Project.query.filter_by(pentest_date=tomorrow).all()
    
    count = 0
    for project in upcoming_projects:
        if send_project_reminder_email(project):
            count += 1
    
    return count 