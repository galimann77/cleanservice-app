from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from core.database import Base
import uuid

class Offer(Base):
    __tablename__ = "offers"
    
    id = Column(Integer, primary_key=True)
    offer_id = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), nullable=False)
    customer_name = Column(String(255))
    total_price = Column(Float, nullable=False)
    data_json = Column(Text) # JSON content of the offer
    created_at = Column(DateTime, server_default=func.now())
    is_public = Column(Integer, default=0)  # 0=privat, 1=teilbar
