from core.database import Base, engine, SessionLocal
from models.master_data import ServiceCategory, ServiceType, CompanySettings
from models.project_data import Project, Room, CleaningTask

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # 1. Seed Company Settings if empty
    if not db.query(CompanySettings).first():
        print("Seeding default company settings...")
        settings = CompanySettings()
        db.add(settings)
    
    # 2. Seed Service Catalog
    # Define known categories and types (subset for startup)
    
    # Categories
    cats = {
        "maintenance": ServiceCategory(id="maintenance", name="Unterhaltsreinigung", icon="🧹"),
        "glass": ServiceCategory(id="glass", name="Glasreinigung", icon="🪟"),
        "special": ServiceCategory(id="special", name="Sonderreinigung", icon="✨"),
        "stone": ServiceCategory(id="stone", name="Steinreinigung", icon="🧱")
    }
    
    for c_id, category in cats.items():
        if not db.query(ServiceCategory).filter_by(id=c_id).first():
            db.add(category)
            
    db.commit() # Commit categories first
    
    # Types
    types = [
        # Maintenance
        ServiceType(id="office_std", category_id="maintenance", name="Büro (Standard)", performance_avg=200, performance_min=170, performance_max=230),
        ServiceType(id="office_full", category_id="maintenance", name="Büro (Volle Möblierung)", performance_avg=150, performance_min=120, performance_max=180),
        ServiceType(id="sanitary", category_id="maintenance", name="Sanitäranlagen", performance_avg=60, performance_min=45, performance_max=80),
        ServiceType(id="corridor", category_id="maintenance", name="Verkehrsflächen", performance_avg=300, performance_min=250, performance_max=350),
        
        # Glass
        ServiceType(id="glass_shop", category_id="glass", name="Schaufenster", performance_avg=100, performance_min=80, performance_max=120, difficulty_factor_default=1.0),
        ServiceType(id="glass_window", category_id="glass", name="Fenster (Dreh-Kipp)", performance_avg=20, performance_min=15, performance_max=25),
        ServiceType(id="glass_box", category_id="glass", name="Kastenfenster", performance_avg=8, performance_min=5, performance_max=12, difficulty_factor_default=1.5),
        
        # Special
        ServiceType(id="floor_basic", category_id="special", name="Grundreinigung Boden", performance_avg=15, price_benchmark_sqm=12.00),
        ServiceType(id="construction_fine", category_id="special", name="Bauendreinigung (Fein)", performance_avg=35, price_benchmark_sqm=6.50),
        
        # Stone
        ServiceType(id="stone_terrace", category_id="stone", name="Terrassenreinigung", performance_avg=40, price_benchmark_sqm=9.00)
    ]
    
    for t in types:
         if not db.query(ServiceType).filter_by(id=t.id).first():
            db.add(t)
            
    db.commit()
    print("Database initialized successfully!")
    db.close()

if __name__ == "__main__":
    init_db()
