import click
from flask.cli import with_appcontext
from app.utils.emails import check_upcoming_pentests
from datetime import datetime

@click.command('send-pentest-reminders')
@with_appcontext
def send_pentest_reminders_command():
    """Send email reminders for projects with pentest dates approaching."""
    click.echo(f"Checking for upcoming pentests on {datetime.now().strftime('%Y-%m-%d')}...")
    
    count = check_upcoming_pentests()
    
    if count > 0:
        click.echo(f"✓ Sent {count} pentest reminder email{'s' if count > 1 else ''}.")
    else:
        click.echo("✓ No upcoming pentests found for tomorrow.")
    
def init_app(app):
    """Register CLI commands with the Flask application."""
    app.cli.add_command(send_pentest_reminders_command) 