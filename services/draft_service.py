from sqlalchemy.orm import Session
from models.draft_model import ProjectDraft
from datetime import datetime
import json

class DraftService:
    @staticmethod
    def auto_save_draft(
        db: Session, 
        user_id: str, 
        project_name: str,
        project_type: str,
        data: dict
    ) -> ProjectDraft:
        """
        Auto-speichert ein Projekt als Draft.
        Update bei existierendem Draft, sonst Insert.
        """
        draft = db.query(ProjectDraft).filter_by(
            user_id=user_id,
            project_name=project_name,
            project_type=project_type
        ).first()
        
        if draft:
            draft.data_json = json.dumps(data, ensure_ascii=False)
            draft.updated_at = datetime.utcnow()
        else:
            draft = ProjectDraft(
                user_id=user_id,
                project_name=project_name,
                project_type=project_type,
                data_json=json.dumps(data, ensure_ascii=False)
            )
            db.add(draft)
        
        db.commit()
        db.refresh(draft)
        return draft
    
    @staticmethod
    def load_latest_draft(
        db: Session, 
        user_id: str,
        project_type: str = None
    ) -> ProjectDraft:
        """
        Laedt neuesten Draft des Users.
        Optional filter nach project_type.
        """
        query = db.query(ProjectDraft).filter_by(user_id=user_id)
        if project_type:
            query = query.filter_by(project_type=project_type)
        return query.order_by(ProjectDraft.updated_at.desc()).first()
    
    @staticmethod
    def list_drafts(db: Session, user_id: str, limit: int = 10):
        """Liste alle Drafts eines Users."""
        return db.query(ProjectDraft).filter_by(
            user_id=user_id
        ).order_by(ProjectDraft.updated_at.desc()).limit(limit).all()
    
    @staticmethod
    def delete_draft(db: Session, draft_id: int):
        """Loescht einen Draft."""
        draft = db.query(ProjectDraft).filter_by(id=draft_id).first()
        if draft:
            db.delete(draft)
            db.commit()
            return True
        return False
