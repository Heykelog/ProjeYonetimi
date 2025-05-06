from app import db
from sqlalchemy.orm import relationship
from datetime import datetime


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manager = db.Column(db.String(100), nullable=False)
    pentest_date = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    project_type = db.Column(db.String(20), nullable=False)  # 'Project' or 'Small Request'
    mandays = db.Column(db.Float, nullable=False, default=0)
    extra_mandays = db.Column(db.Float, nullable=True, default=0)
    extra_mandays_reason = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(200), nullable=True)  # Etiketler için virgülle ayrılmış liste
    is_backlog = db.Column(db.Boolean, default=False)  # Backlog durumu
    priority = db.Column(db.Integer, default=0)  # Backlog önceliği
    
    # Foreign keys
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="projects")
    findings = relationship("Finding", back_populates="project", cascade="all, delete-orphan")
    
    def __init__(self, name, manager, pentest_date, project_type, mandays, company_id, completed=False, 
                 extra_mandays=0, extra_mandays_reason=None, tags=None, is_backlog=False, priority=0):
        self.name = name
        self.manager = manager
        self.pentest_date = pentest_date
        self.project_type = project_type
        self.mandays = mandays
        self.company_id = company_id
        self.completed = completed
        self.extra_mandays = extra_mandays
        self.extra_mandays_reason = extra_mandays_reason
        self.tags = tags
        self.is_backlog = is_backlog
        self.priority = priority
    
    def findings_by_severity(self):
        severity_counts = {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        }
        
        for finding in self.findings:
            severity_counts[finding.severity] += 1
                
        return severity_counts
    
    def get_tags_list(self):
        """Etiketleri liste olarak döndür"""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',')]
    
    def add_tag(self, tag):
        """Projeye yeni etiket ekle"""
        current_tags = self.get_tags_list()
        if tag not in current_tags:
            current_tags.append(tag)
            self.tags = ', '.join(current_tags)
    
    def remove_tag(self, tag):
        """Projeden etiket kaldır"""
        current_tags = self.get_tags_list()
        if tag in current_tags:
            current_tags.remove(tag)
            self.tags = ', '.join(current_tags) if current_tags else None 