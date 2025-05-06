from app import db
from sqlalchemy.orm import relationship


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    total_mandays = db.Column(db.Float, nullable=False, default=0)
    
    # Relationships
    projects = relationship("Project", back_populates="company", cascade="all, delete-orphan")
    
    def __init__(self, name, total_mandays):
        self.name = name
        self.total_mandays = total_mandays
    
    def remaining_mandays(self):
        used_mandays = sum((project.mandays + (project.extra_mandays or 0)) for project in self.projects)
        return self.total_mandays - used_mandays
    
    def completed_projects_count(self):
        return sum(1 for project in self.projects if project.completed)
    
    def ongoing_projects_count(self):
        return sum(1 for project in self.projects if not project.completed)
    
    def total_findings_count(self):
        count = 0
        for project in self.projects:
            count += len(project.findings)
        return count
    
    def findings_by_severity(self):
        severity_counts = {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        }
        
        for project in self.projects:
            for finding in project.findings:
                severity_counts[finding.severity] += 1
                
        return severity_counts 