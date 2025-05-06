from app import create_app, db
from app.models.company import Company
from app.models.project import Project
from app.models.finding import Finding
from datetime import datetime, timedelta
import random

def create_dummy_data():
    # Create app context
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Create companies
        companies = [
            Company(name="TechCorp Inc.", total_mandays=30),
            Company(name="Secure Systems LLC", total_mandays=45),
            Company(name="DataGuard Solutions", total_mandays=20),
            Company(name="Cyber Defense Partners", total_mandays=15)
        ]
        
        for company in companies:
            db.session.add(company)
        
        db.session.commit()
        
        # Create projects
        today = datetime.now().date()
        project_types = ["Project", "Small Request"]
        manager_names = ["John Smith", "Maria Garcia", "David Wang", "Sarah Johnson", "Ahmed Ali"]
        
        projects = []
        for company in companies:
            num_projects = random.randint(2, 5)
            for i in range(num_projects):
                completed = random.choice([True, False])
                pentest_date = today - timedelta(days=random.randint(0, 90))
                
                project = Project(
                    name=f"Project {i+1} for {company.name}",
                    manager=random.choice(manager_names),
                    pentest_date=pentest_date,
                    project_type=random.choice(project_types),
                    mandays=random.randint(1, 10),
                    company_id=company.id,
                    completed=completed
                )
                
                db.session.add(project)
                projects.append(project)
        
        db.session.commit()
        
        # Create findings
        severity_levels = ["Critical", "High", "Medium", "Low"]
        statuses = ["Open", "Closed"]
        
        finding_names = [
            "SQL Injection Vulnerability", 
            "Cross-Site Scripting (XSS)", 
            "Insecure Direct Object References",
            "Security Misconfiguration", 
            "Broken Authentication", 
            "Sensitive Data Exposure",
            "Missing Function Level Access Control", 
            "Cross-Site Request Forgery (CSRF)",
            "Using Components with Known Vulnerabilities", 
            "Unvalidated Redirects and Forwards",
            "Weak Password Policy", 
            "Insecure Cryptographic Storage",
            "Insufficient Logging & Monitoring", 
            "Server-Side Request Forgery (SSRF)",
            "XML External Entity (XXE) Injection"
        ]
        
        for project in projects:
            num_findings = random.randint(3, 8)
            for i in range(num_findings):
                severity = random.choice(severity_levels)
                status = random.choice(statuses)
                
                # More serious findings are more likely to be open
                if severity in ["Critical", "High"] and random.random() < 0.7:
                    status = "Open"
                
                # Generate a random finding name from the list
                finding_name = random.choice(finding_names)
                
                finding = Finding(
                    name=finding_name,
                    severity=severity,
                    description=f"This is a {severity.lower()} severity finding that affects the system. Detailed steps to reproduce and remediation advice would be included here.",
                    status=status,
                    project_id=project.id
                )
                
                db.session.add(finding)
        
        db.session.commit()
        
        print("Dummy data has been created successfully!")
        print(f"Created {len(companies)} companies, {len(projects)} projects, and multiple findings.")

if __name__ == "__main__":
    create_dummy_data() 