from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

# class CompanySettings(Base):
#     """Global company settings and cost parameters."""
#     __tablename__ = "company_settings"
#
#     id = Column(Integer, primary_key=True, index=True)
#     
#     # Company Info
#     company_name = Column(String, default="Mein Reinigungsunternehmen")
#     address = Column(String, default="")
#     tax_id = Column(String, default="")
#     
#     # Wages (Hourly Rates in €)
#     wage_maintenance = Column(Float, default=18.40) # Unterhalt
#     wage_glass = Column(Float, default=20.00)       # Glas
#     wage_special = Column(Float, default=19.50)     # Sonder
#     
#     # Factors (%)
#     social_security_percent = Column(Float, default=80.0) # Lohnnebenkosten (AG-Anteil, Urlaub, Krank)
#     material_percent = Column(Float, default=5.0)
#     equipment_percent = Column(Float, default=2.0)
#     overhead_percent = Column(Float, default=15.0)
#     profit_margin_percent = Column(Float, default=25.0) # Zielmarge
#     
#     # Surcharges (%)
#     surcharge_night = Column(Float, default=25.0)
#     surcharge_sunday = Column(Float, default=50.0)
#     surcharge_holiday = Column(Float, default=125.0)
#     
#     # Settings
#     currency = Column(String, default="EUR")
#     vat_percent = Column(Float, default=19.0)


class ServiceCategory(Base):
    """Category of cleaning service (e.g. Unterhaltsreinigung, Glasreinigung)."""
    __tablename__ = "service_categories"
    
    id = Column(String, primary_key=True) # e.g. "maintenance", "glass"
    name = Column(String, nullable=False)
    icon = Column(String, default="🧹")
    description = Column(String)
    
    types = relationship("ServiceType", back_populates="category")


class ServiceType(Base):
    """Specific cleaning service type (e.g. Büro Standard, Schaufenster)."""
    __tablename__ = "service_types"
    
    id = Column(String, primary_key=True) # e.g. "office_std"
    category_id = Column(String, ForeignKey("service_categories.id"))
    name = Column(String, nullable=False)
    
    # Performance benchmarks (m²/h)
    performance_avg = Column(Float, nullable=False)
    performance_min = Column(Float)
    performance_max = Column(Float)
    
    # OR Fixed Price Benchmark (€/m² - optional alternative)
    price_benchmark_sqm = Column(Float, nullable=True)
    
    description = Column(String)
    difficulty_factor_default = Column(Float, default=1.0)
    
    category = relationship("ServiceCategory", back_populates="types")
