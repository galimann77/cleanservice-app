from sqlalchemy.orm import Session
from models.data_models import ProjectDraftDB, ProjectDraft
import json
from datetime import datetime

class StateService:
    @staticmethod
    def ensure_tables(engine):
        from models.data_models import Base
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def save_draft(db: Session, user_id: str, name: str, data: dict):
        # Check if draft exists for this name/user
        existing = db.query(ProjectDraftDB).filter(
            ProjectDraftDB.user_id == user_id, 
            ProjectDraftDB.name == name
        ).first()

        json_data = json.dumps(data, default=str)

        if existing:
            existing.data_json = json_data
            existing.updated_at = datetime.utcnow()
        else:
            draft = ProjectDraftDB(
                user_id=user_id,
                name=name,
                data_json=json_data
            )
            db.add(draft)
        
        db.commit()

    @staticmethod
    def load_latest_draft(db: Session, user_id: str):
        draft = db.query(ProjectDraftDB).filter(
            ProjectDraftDB.user_id == user_id
        ).order_by(ProjectDraftDB.updated_at.desc()).first()
        
        if draft:
            return json.loads(draft.data_json)
        return None

    @staticmethod
    def list_drafts(db: Session, user_id: str):
         return db.query(ProjectDraftDB).filter(
            ProjectDraftDB.user_id == user_id
        ).order_by(ProjectDraftDB.updated_at.desc()).all()
