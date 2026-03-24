from core.database import get_db
from models.company_settings import CompanySettings
import streamlit as st

def show_stammdaten():
    st.title("⚙️ Stammdaten & Kostenparameter")
    st.caption("Globale Berechnungsgrundlage")
    
    db = next(get_db())
    try:
        settings = db.query(CompanySettings).first()
        
        if not settings:
            st.error("❌ Keine Stammdaten")
            if st.button("🔧 Defaults erstellen"):
                from core.init_db import init_default_company_settings
                init_default_company_settings()
                st.rerun()
            return
        
        tab1, tab2 = st.tabs(["Firmendaten", "Kalkulation"])
        
        with tab1:
            st.subheader("Firmendaten")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Firma", value=settings.company_name)
                street = st.text_input("Straße", value=settings.street or "")
                city = st.text_input("Stadt", value=settings.city or "")
            with col2:
                plz = st.text_input("PLZ", value=settings.postal_code or "")
                phone = st.text_input("Telefon", value=settings.phone or "")
                email = st.text_input("E-Mail", value=settings.email or "")
        
        with tab2:
            st.subheader("Kalkulationsparameter")
            col_a, col_b = st.columns(2)
            with col_a:
                rate = st.number_input("Stundensatz (€)", 
                    min_value=10.0, max_value=100.0, 
                    value=float(settings.hourly_rate), step=0.5)
                vat = st.number_input("MwSt (%)", 
                    min_value=0.0, max_value=30.0, 
                    value=float(settings.vat_rate), step=1.0)
            with col_b:
                margin = st.number_input("Gewinnmarge (%)", 
                    min_value=0.0, max_value=50.0, 
                    value=float(settings.profit_margin), step=1.0)
                setup = st.number_input("Rüstzeiten (%)", 
                    min_value=0.0, max_value=30.0, 
                    value=float(settings.setup_time_percentage), step=1.0)
        
        st.divider()
        if st.button("💾 Speichern", type="primary"):
            settings.company_name = name
            settings.street = street
            settings.city = city
            settings.postal_code = plz
            settings.phone = phone
            settings.email = email
            settings.hourly_rate = rate
            settings.vat_rate = vat
            settings.profit_margin = margin
            settings.setup_time_percentage = setup
            db.commit()
            st.success("✅ Gespeichert!")
            st.rerun()
    finally:
        db.close()
