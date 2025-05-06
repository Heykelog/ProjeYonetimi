from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.models.project import Project
from app.models.company import Company
from app.forms.project import ProjectForm
from app.utils.emails import send_project_reminder_email
from datetime import datetime, timedelta

project_bp = Blueprint('project', __name__)

@project_bp.route('/')
def index():
    tag = request.args.get('tag')
    if tag:
        projects = Project.query.filter(
            Project.tags.like(f'%{tag}%'),
            Project.is_backlog == False
        ).all()
        title = f'"{tag}" Etiketli Projeler'
    else:
        projects = Project.query.filter_by(is_backlog=False).all()
        title = 'Projeler'
    
    return render_template('project/index.html', projects=projects, title=title)

@project_bp.route('/calendar')
def calendar():
    return render_template('project/calendar.html', title='Proje Takvimi')

@project_bp.route('/api/calendar-events')
def calendar_events():
    start_date = request.args.get('start', None)
    end_date = request.args.get('end', None)
    
    if start_date and end_date:
        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    else:
        # Varsayılan olarak önümüzdeki 3 ay
        start_date = datetime.now()
        end_date = start_date + timedelta(days=90)
    
    projects = Project.query.filter(
        Project.pentest_date >= start_date,
        Project.pentest_date <= end_date
    ).all()
    
    events = []
    for project in projects:
        # Tamamlanmış projelere farklı renk
        color = '#28a745' if project.completed else '#ffc107'
        
        # Bugün başlayan projeleri vurgula
        if isinstance(project.pentest_date, datetime):
            project_date = project.pentest_date.date()
        else:
            project_date = project.pentest_date
            
        if project_date == datetime.now().date():
            color = '#dc3545'  # Kırmızı
        
        # Proje türüne göre simge
        title_prefix = "🔍" if project.project_type == 'Proje' else "🔎"
        
        events.append({
            'id': project.id,
            'title': f"{title_prefix} {project.name}",
            'start': project.pentest_date.isoformat(),
            'color': color,
            'extendedProps': {
                'company': project.company.name,
                'manager': project.manager,
                'mandays': project.mandays,
                'completed': project.completed,
                'project_type': project.project_type
            },
            'url': url_for('project.view', id=project.id)
        })
    
    return jsonify(events)

@project_bp.route('/new', methods=['GET', 'POST'])
def new():
    form = ProjectForm()
    form.company_id.choices = [(c.id, c.name) for c in Company.query.all()]
    
    if form.validate_on_submit():
        project = Project(
            name=form.name.data,
            manager=form.manager.data,
            pentest_date=form.pentest_date.data,
            project_type=form.project_type.data,
            mandays=form.mandays.data,
            company_id=form.company_id.data,
            completed=form.completed.data,
            extra_mandays=form.extra_mandays.data,
            extra_mandays_reason=form.extra_mandays_reason.data,
            tags=form.tags.data,
            is_backlog=form.is_backlog.data,
            priority=form.priority.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('project.index'))
    
    return render_template('project/form.html', form=form, title='Add Project')

@project_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    form.company_id.choices = [(c.id, c.name) for c in Company.query.all()]
    
    if form.validate_on_submit():
        project.name = form.name.data
        project.manager = form.manager.data
        project.pentest_date = form.pentest_date.data
        project.project_type = form.project_type.data
        project.mandays = form.mandays.data
        project.company_id = form.company_id.data
        project.completed = form.completed.data
        project.extra_mandays = form.extra_mandays.data
        project.extra_mandays_reason = form.extra_mandays_reason.data
        project.tags = form.tags.data
        project.is_backlog = form.is_backlog.data
        project.priority = form.priority.data
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('project.index'))
    
    return render_template('project/form.html', form=form, title='Edit Project')

@project_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('project.index'))

@project_bp.route('/<int:id>')
def view(id):
    project = Project.query.get_or_404(id)
    return render_template('project/view.html', project=project)

@project_bp.route('/<int:id>/send-reminder', methods=['POST'])
def send_reminder(id):
    project = Project.query.get_or_404(id)
    
    if send_project_reminder_email(project):
        flash('Pentest hatırlatma e-postası başarıyla gönderildi!', 'success')
    else:
        flash('E-posta gönderilirken bir hata oluştu. Lütfen sistem yöneticisiyle iletişime geçin.', 'danger')
    
    return redirect(url_for('project.view', id=project.id))

@project_bp.route('/backlog')
def backlog():
    """Backlog projelerini görüntüle"""
    backlog_projects = Project.query.filter_by(is_backlog=True).order_by(Project.priority.desc()).all()
    return render_template('project/backlog.html', projects=backlog_projects, title='Proje Backlog')

@project_bp.route('/tags/<tag>')
def by_tag(tag):
    """Etikete göre projeleri filtrele"""
    projects = Project.query.filter(Project.tags.like(f'%{tag}%')).all()
    return render_template('project/index.html', projects=projects, title=f'"{tag}" Etiketli Projeler')

@project_bp.route('/add_to_backlog/<int:id>', methods=['POST'])
def add_to_backlog(id):
    """Projeyi backlog'a ekle"""
    project = Project.query.get_or_404(id)
    project.is_backlog = True
    db.session.commit()
    flash('Proje backlog\'a eklendi!', 'success')
    return redirect(url_for('project.view', id=project.id))

@project_bp.route('/remove_from_backlog/<int:id>', methods=['POST'])
def remove_from_backlog(id):
    """Projeyi backlog'dan çıkar"""
    project = Project.query.get_or_404(id)
    project.is_backlog = False
    db.session.commit()
    flash('Proje backlog\'dan çıkarıldı!', 'success')
    return redirect(url_for('project.view', id=project.id)) 