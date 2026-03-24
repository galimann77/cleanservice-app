from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Project(Base):
    """A calculation project (Offer)."""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # e.g. "Office Park West"
    customer_name = Column(String)
    created_at = Column(Date, default=datetime.utcnow)
    status = Column(String, default="Draft") # Draft, Sent, Won, Lost
    
    # Relationships
    rooms = relationship("Room", back_populates="project", cascade="all, delete-orphan")
    
    # Calculated Totals (Cached/Denormalized for Speed)
    total_area = Column(Float, default=0.0)
    total_price_net = Column(Float, default=0.0)
    total_hours_monthly = Column(Float, default=0.0)

class Room(Base):
    """A physical room in a project."""
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    name = Column(String, nullable=False) # e.g. "Office 101"
    room_type = Column(String) # e.g. "Büro", "WC", "Flur" -> mapped to ServiceCategory usually
    area_sqm = Column(Float, nullable=False)
    floor_type = Column(String) # e.g. "Teppich", "PVC"
    photos_json = Column(Text, default="[]") # JSON list of file paths/references
    
    project = relationship("Project", back_populates="rooms")
    tasks = relationship("CleaningTask", back_populates="room", cascade="all, delete-orphan")

class CleaningTask(Base):
    """A specific cleaning activity in a room (The "Planstelle")."""
    __tablename__ = "cleaning_tasks"
    
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    
    # Link to Service Catalog
    service_type_id = Column(String, ForeignKey("service_types.id"))
    
    # Parameters
    frequency_per_year = Column(Integer, default=250) # e.g. 5x week = 250
    interval_factor = Column(Float, default=1.0)
    difficulty_factor = Column(Float, default=1.0)
    
    # Calculated Values (Persisted for Freeze/Snapshot)
    performance_used = Column(Float) # m²/h used
    minutes_per_service = Column(Float)
    hours_per_month = Column(Float)
    labor_cost_per_month = Column(Float)
    price_net_monthly = Column(Float)
    
    room = relationship("Room", back_populates="tasks")
    service_type = relationship("ServiceType") # Unidirectional link to catalog
