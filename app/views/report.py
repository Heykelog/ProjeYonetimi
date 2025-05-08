from flask import Blueprint, render_template, make_response, send_file, request
from app.models.company import Company
from app.models.project import Project
from app.models.finding import Finding
import io
import csv
from datetime import datetime
from sqlalchemy import or_

report_bp = Blueprint('report', __name__)

@report_bp.route('/')
def index():
    companies = Company.query.all()
    
    company_stats = []
    for company in companies:
        stats = {
            'id': company.id,
            'name': company.name,
            'total_mandays': company.total_mandays,
            'used_mandays': company.total_mandays - company.remaining_mandays(),
            'remaining_mandays': company.remaining_mandays(),
            'completed_projects': company.completed_projects_count(),
            'ongoing_projects': company.ongoing_projects_count(),
            'total_findings': company.total_findings_count(),
            'findings_by_severity': company.findings_by_severity()
        }
        company_stats.append(stats)
        
    return render_template('report/index.html', company_stats=company_stats)

@report_bp.route('/company/<int:company_id>')
def company_report(company_id):
    company = Company.query.get_or_404(company_id)
    projects = Project.query.filter_by(company_id=company_id).all()
    
    return render_template('report/company.html', company=company, projects=projects)

@report_bp.route('/extra-mandays')
def extra_mandays_report():
    company_id = request.args.get('company_id', type=int)
    
    if company_id:
        # Filter by company if provided
        projects = Project.query.filter(
            Project.company_id == company_id,
            Project.extra_mandays > 0
        ).order_by(Project.pentest_date.desc()).all()
        company = Company.query.get_or_404(company_id)
        title = f"Ek Adam-Gün Raporu - {company.name}"
    else:
        # Get all projects with extra mandays
        projects = Project.query.filter(
            Project.extra_mandays > 0
        ).order_by(Project.pentest_date.desc()).all()
        company = None
        title = "Ek Adam-Gün Raporu - Tüm Şirketler"
    
    # Get all companies for the filter dropdown
    companies = Company.query.all()
    
    return render_template(
        'report/extra_mandays.html', 
        projects=projects, 
        companies=companies,
        selected_company_id=company_id,
        title=title
    )

@report_bp.route('/export/extra-mandays')
def export_extra_mandays_report():
    company_id = request.args.get('company_id', type=int)
    
    if company_id:
        # Filter by company if provided
        projects = Project.query.filter(
            Project.company_id == company_id,
            Project.extra_mandays > 0
        ).order_by(Project.pentest_date.desc()).all()
        company = Company.query.get_or_404(company_id)
        filename = f"ek_adam_gun_raporu_{company.name}_{datetime.now().strftime('%Y%m%d')}.csv"
    else:
        # Get all projects with extra mandays
        projects = Project.query.filter(
            Project.extra_mandays > 0
        ).order_by(Project.pentest_date.desc()).all()
        filename = f"ek_adam_gun_raporu_tum_sirketler_{datetime.now().strftime('%Y%m%d')}.csv"
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Ek Adam-Gün Raporu', datetime.now().strftime('%Y-%m-%d')])
    writer.writerow([])
    writer.writerow(['Proje Adı', 'Şirket', 'Yönetici', 'Pentest Tarihi', 'Proje Türü', 'Planlanan A/G', 'Ek A/G', 'Toplam A/G', 'Ek A/G Nedeni', 'Durum'])
    
    # Write project data
    for project in projects:
        writer.writerow([
            project.name,
            project.company.name,
            project.manager,
            project.pentest_date.strftime('%Y-%m-%d'),
            project.project_type,
            project.mandays,
            project.extra_mandays,
            project.mandays + project.extra_mandays,
            project.extra_mandays_reason or '',
            'Tamamlandı' if project.completed else 'Devam Ediyor'
        ])
    
    # Create response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.headers['Content-type'] = 'text/csv'
    
    return response

@report_bp.route('/export/company/<int:company_id>')
def export_company_report(company_id):
    company = Company.query.get_or_404(company_id)
    projects = Project.query.filter_by(company_id=company_id).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Company Report', company.name, datetime.now().strftime('%Y-%m-%d')])
    writer.writerow([])
    writer.writerow(['Company Statistics'])
    writer.writerow(['Total Man-days', 'Used Man-days', 'Remaining Man-days', 'Completed Projects', 'Ongoing Projects', 'Total Findings'])
    
    # Write company stats
    writer.writerow([
        company.total_mandays,
        company.total_mandays - company.remaining_mandays(),
        company.remaining_mandays(),
        company.completed_projects_count(),
        company.ongoing_projects_count(),
        company.total_findings_count()
    ])
    
    # Write findings by severity
    writer.writerow([])
    writer.writerow(['Findings by Severity'])
    severity_stats = company.findings_by_severity()
    writer.writerow(['Critical', 'High', 'Medium', 'Low'])
    writer.writerow([
        severity_stats['Critical'],
        severity_stats['High'],
        severity_stats['Medium'],
        severity_stats['Low']
    ])
    
    # Write projects
    writer.writerow([])
    writer.writerow(['Projects'])
    writer.writerow(['Name', 'Manager', 'Pentest Date', 'Type', 'Man-days', 'Extra Man-days', 'Total Man-days', 'Status', 'Findings'])
    
    for project in projects:
        writer.writerow([
            project.name,
            project.manager,
            project.pentest_date.strftime('%Y-%m-%d'),
            project.project_type,
            project.mandays,
            project.extra_mandays or 0,
            project.mandays + (project.extra_mandays or 0),
            'Tamamlandı' if project.completed else 'Devam Ediyor',
            len(project.findings)
        ])
    
    # Create response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=company_report_{company.name}_{datetime.now().strftime("%Y%m%d")}.csv'
    response.headers['Content-type'] = 'text/csv'
    
    return response

@report_bp.route('/projects-report')
def projects_report():
    company_id = request.args.get('company_id', type=int)
    project_type = request.args.get('project_type', type=str)
    
    # Base query
    query = Project.query
    
    # Apply filters if provided
    if company_id:
        query = query.filter(Project.company_id == company_id)
    
    if project_type and project_type.strip():  # Boş string kontrolü ekledik
        query = query.filter(Project.project_type == project_type)
    
    # Get all projects sorted by date
    projects = query.order_by(Project.pentest_date.desc()).all()
    
    # Get all companies for the filter dropdown
    companies = Company.query.all()
    
    # Get statistics
    total_projects = len(projects)
    total_mandays = sum(p.mandays + (p.extra_mandays or 0) for p in projects)
    
    # Calculate stats by project type
    stats_by_type = {}
    for p in projects:
        if p.project_type not in stats_by_type:
            stats_by_type[p.project_type] = {
                'count': 0,
                'total_mandays': 0
            }
        stats_by_type[p.project_type]['count'] += 1
        stats_by_type[p.project_type]['total_mandays'] += p.mandays + (p.extra_mandays or 0)
    
    return render_template(
        'report/projects_report.html',
        projects=projects,
        companies=companies,
        selected_company_id=company_id,
        selected_project_type=project_type,
        total_projects=total_projects,
        total_mandays=total_mandays,
        stats_by_type=stats_by_type
    )

@report_bp.route('/export/projects-report')
def export_projects_report():
    company_id = request.args.get('company_id', type=int)
    project_type = request.args.get('project_type', type=str)
    
    # Base query
    query = Project.query
    
    # Apply filters if provided
    if company_id:
        query = query.filter(Project.company_id == company_id)
        company = Company.query.get_or_404(company_id)
        company_name = company.name
    else:
        company_name = "Tüm Şirketler"
    
    if project_type:
        query = query.filter(Project.project_type == project_type)
        type_label = project_type
    else:
        type_label = "Tüm Projeler"
    
    # Get all projects sorted by date
    projects = query.order_by(Project.pentest_date.desc()).all()
    
    filename = f"proje_raporu_{company_name}_{type_label}_{datetime.now().strftime('%Y%m%d')}.csv"
    filename = filename.replace(" ", "_")
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Proje Raporu', f'{company_name} - {type_label}', datetime.now().strftime('%Y-%m-%d')])
    writer.writerow([])
    
    # Write summary
    writer.writerow(['Özet'])
    writer.writerow(['Toplam Proje Sayısı', 'Toplam Adam/Gün'])
    writer.writerow([len(projects), sum(p.mandays + (p.extra_mandays or 0) for p in projects)])
    writer.writerow([])
    
    # Write project data
    writer.writerow(['Proje Adı', 'Şirket', 'Yönetici', 'Pentest Tarihi', 'Proje Türü', 'Planlanan A/G', 'Ek A/G', 'Toplam A/G', 'Bulgular', 'Durum'])
    
    for project in projects:
        writer.writerow([
            project.name,
            project.company.name,
            project.manager,
            project.pentest_date.strftime('%Y-%m-%d'),
            project.project_type,
            project.mandays,
            project.extra_mandays or 0,
            project.mandays + (project.extra_mandays or 0),
            len(project.findings),
            'Tamamlandı' if project.completed else 'Devam Ediyor'
        ])
    
    # Create response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.headers['Content-type'] = 'text/csv'
    
    return response 