from sqlalchemy.orm import Session
from models.project_data import Project, Room, CleaningTask
from models.master_data import ServiceType
from datetime import datetime

class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, name: str, customer: str = "") -> Project:
        proj = Project(name=name, customer_name=customer, status="Draft")
        self.db.add(proj)
        self.db.commit()
        self.db.refresh(proj)
        return proj

    def get_projects(self):
        return self.db.query(Project).order_by(Project.created_at.desc()).all()

    def get_project(self, project_id: int) -> Project:
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def add_room(self, project_id: int, name: str, area: float, room_type: str) -> Room:
        room = Room(project_id=project_id, name=name, area_sqm=area, room_type=room_type)
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room
    
    def add_task(self, room_id: int, service_id: str, freq: int = 250) -> CleaningTask:
        task = CleaningTask(room_id=room_id, service_type_id=service_id, frequency_per_year=freq)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete_room(self, room_id: int):
        room = self.db.query(Room).filter(Room.id == room_id).first()
        if room:
            self.db.delete(room)
            self.db.commit()
            
    def delete_task(self, task_id: int):
        task = self.db.query(CleaningTask).filter(CleaningTask.id == task_id).first()
        if task:
            self.db.delete(task)
            self.db.commit()
