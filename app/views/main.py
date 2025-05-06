from flask import Blueprint, render_template, redirect, url_for
from app.models.company import Company
from app.models.project import Project
from app.models.finding import Finding
from datetime import datetime, timedelta
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Temel sayısal bilgiler
    companies_count = Company.query.count()
    projects_count = Project.query.count()
    completed_projects = Project.query.filter_by(completed=True).count()
    ongoing_projects = Project.query.filter_by(completed=False).count()
    findings_count = Finding.query.count()
    
    # Yaklaşan pentestler (bir hafta içinde)
    today = datetime.now().date()
    one_week_later = today + timedelta(days=7)
    upcoming_pentests = Project.query.filter(
        Project.pentest_date >= today,
        Project.pentest_date <= one_week_later,
        Project.completed == False
    ).order_by(Project.pentest_date).all()
    
    # Adam-gün havuzu neredeyse tükenmiş şirketler (kalan havuzun %20'sinden azı)
    low_mandays_companies = Company.query.all()
    low_mandays_companies = [
        company for company in low_mandays_companies 
        if company.remaining_mandays() <= (company.total_mandays * 0.2) and company.remaining_mandays() > 0
    ]
    
    # Bugün başlaması gereken pentestler
    today_pentests = Project.query.filter(
        func.date(Project.pentest_date) == today,
        Project.completed == False
    ).all()
    
    # Kritik/Yüksek öncelikli açık bulgular
    critical_findings = Finding.query.filter(
        Finding.severity.in_(['Critical', 'High']), 
        Finding.status == 'Open'
    ).count()
    
    # En son eklenen projeler
    recent_projects = Project.query.order_by(Project.id.desc()).limit(5).all()
    
    # Şirketlere göre toplam bulgular
    companies = Company.query.all()
    company_findings = []
    for company in companies:
        total_findings = sum(len(project.findings) for project in company.projects)
        if total_findings > 0:
            company_findings.append({
                'company': company,
                'findings': total_findings
            })
    company_findings = sorted(company_findings, key=lambda x: x['findings'], reverse=True)[:5]
    
    return render_template('index.html', 
                           companies_count=companies_count,
                           projects_count=projects_count,
                           completed_projects=completed_projects,
                           ongoing_projects=ongoing_projects,
                           findings_count=findings_count,
                           upcoming_pentests=upcoming_pentests,
                           low_mandays_companies=low_mandays_companies,
                           today_pentests=today_pentests,
                           critical_findings=critical_findings,
                           recent_projects=recent_projects,
                           company_findings=company_findings,
                           today=today) 