from core.database import get_db, Base, get_engine
from models.company_settings import CompanySettings
from models.master_data import ServiceCategory, ServiceType
from services.calculation import CalculationService

def init_master_data():
    db = next(get_db())
    try:
        # Check if we have data
        if db.query(ServiceType).first():
            print("✅ Master Data (Services) already exists.")
            return

        print("🔧 Seeding Master Data from JSON...")
        calc_service = CalculationService() # Loads JSON
        
        # 1. Categories
        categories = set()
        for ct in calc_service.get_cleaning_types():
            categories.add(ct.category)
            
        category_map = {}
        for cat_name in categories:
            # Simple ID generation
            cat_id = cat_name.lower().replace(" ", "_")
            category = ServiceCategory(
                id=cat_id,
                name=cat_name,
                description=cat_name
            )
            db.merge(category) # Use merge to avoid duplicates if partial data
            category_map[cat_name] = cat_id
            
        db.commit()
        
        # 2. Service Types
        count = 0
        for ct in calc_service.get_cleaning_types():
            cat_id = category_map.get(ct.category)
            
            st_obj = ServiceType(
                id=ct.id,
                category_id=cat_id,
                name=ct.name,
                performance_avg=ct.performance_sqm_per_h.avg,
                performance_min=ct.performance_sqm_per_h.min,
                performance_max=ct.performance_sqm_per_h.max,
                description=ct.description
            )
            db.merge(st_obj)
            count += 1
            
        db.commit()
        print(f"✅ Created {len(categories)} Categories and {count} Service Types.")
        
    except Exception as e:
        print(f"❌ Master Data Init Error: {e}")
        db.rollback()
    finally:
        db.close()

def init_default_company_settings():
    db = next(get_db()) # get_db is generator
    try:
        existing = db.query(CompanySettings).first()
        if not existing:
            print("🔧 Erstelle Default Company Settings...")
            default = CompanySettings(
                company_name="Ihr Reinigungsservice",
                street="Musterstraße 1",
                city="Musterstadt",
                postal_code="12345",
                phone="+49 123 456789",
                email="info@reinigung.de",
                hourly_rate=25.00,
                vat_rate=19.0,
                profit_margin=15.0,
                setup_time_percentage=10.0
            )
            db.add(default)
            db.commit()
            print(f"✅ Settings erstellt: {default.company_name}")
        else:
            print(f"✅ Settings OK: {existing.company_name}")
    except Exception as e:
        print(f"❌ Fehler: {e}")
        db.rollback()
    finally:
        db.close()

def init_all_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("✅ Tabellen erstellt")

def init_database():
    print("="*70)
    print("CLEANSERVICE - DB Init")
    print("="*70)
    init_all_tables()
    init_default_company_settings()
    init_master_data()
    print("="*70)
