from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models.finding import Finding
from app.models.project import Project
from app.forms.finding import FindingForm

finding_bp = Blueprint('finding', __name__)

@finding_bp.route('/')
def all_findings():
    findings = Finding.query.all()
    return render_template('finding/all.html', findings=findings)

@finding_bp.route('/project/<int:project_id>')
def index(project_id):
    project = Project.query.get_or_404(project_id)
    findings = Finding.query.filter_by(project_id=project_id).all()
    return render_template('finding/index.html', findings=findings, project=project)

@finding_bp.route('/project/<int:project_id>/new', methods=['GET', 'POST'])
def new(project_id):
    project = Project.query.get_or_404(project_id)
    form = FindingForm()
    
    if form.validate_on_submit():
        finding = Finding(
            name=form.name.data,
            severity=form.severity.data,
            description=form.description.data,
            status=form.status.data,
            project_id=project_id
        )
        db.session.add(finding)
        db.session.commit()
        flash('Finding added successfully!', 'success')
        return redirect(url_for('finding.index', project_id=project_id))
    
    return render_template('finding/form.html', form=form, project=project, title='Add Finding')

@finding_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    finding = Finding.query.get_or_404(id)
    form = FindingForm(obj=finding)
    
    if form.validate_on_submit():
        finding.name = form.name.data
        finding.severity = form.severity.data
        finding.description = form.description.data
        finding.status = form.status.data
        
        db.session.commit()
        flash('Finding updated successfully!', 'success')
        return redirect(url_for('finding.index', project_id=finding.project_id))
    
    return render_template('finding/form.html', form=form, project=finding.project, title='Edit Finding')

@finding_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    finding = Finding.query.get_or_404(id)
    project_id = finding.project_id
    db.session.delete(finding)
    db.session.commit()
    flash('Finding deleted successfully!', 'success')
    return redirect(url_for('finding.index', project_id=project_id)) 