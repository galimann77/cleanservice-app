from sqlalchemy import Column, Integer, String, Text, DateTime
from core.database import Base
from datetime import datetime

class ProjectDraft(Base):
    __tablename__ = "project_drafts"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="default_user", index=True)
    project_name = Column(String, nullable=True)
    project_type = Column(String, default="raumbuch")  # raumbuch, vob, schnell
    data_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProjectDraft {self.project_name} ({self.project_type})>"
