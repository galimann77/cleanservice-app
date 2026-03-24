from sqlalchemy import Column, Integer, String, Float
from core.database import Base

class CompanySettings(Base):
    __tablename__ = "company_settings"
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), default="Reinigungsservice")
    street = Column(String(255))
    city = Column(String(255))
    postal_code = Column(String(10))
    phone = Column(String(50))
    email = Column(String(100))
    hourly_rate = Column(Float, default=25.00)
    vat_rate = Column(Float, default=19.0)
    profit_margin = Column(Float, default=15.0)
    setup_time_percentage = Column(Float, default=10.0)
