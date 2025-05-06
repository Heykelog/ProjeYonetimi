from app import db
from sqlalchemy.orm import relationship


class Finding(db.Model):
    __tablename__ = 'findings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # 'Critical', 'High', 'Medium', 'Low'
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Open')  # 'Open' or 'Closed'
    
    # Foreign keys
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="findings")
    
    def __init__(self, name, severity, project_id, description=None, status='Open'):
        self.name = name
        self.severity = severity
        self.project_id = project_id
        self.description = description
        self.status = status 