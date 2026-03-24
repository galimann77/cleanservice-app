import streamlit as st
from models.master_data import CompanySettings
from sqlalchemy.orm import Session
from services.price_db_service import PriceDatabaseService

def render_master_data_editor(db: Session):
    st.title("⚙️ Stammdaten & Kostenparameter")
    st.info("Hier definieren Sie die globale Berechnungsgrundlage.")
    
    settings = db.query(CompanySettings).first()
    if not settings:
        st.error("Keine Stammdaten gefunden.")
        return

    # Create Tabs
    tab1, tab2, tab4 = st.tabs(["Stammdaten & Faktoren", "Reinigungsarten", "Preisdatenbank 🆕"])
    
    # --- TAB 1: Unternehmensdaten & Faktoren ---
    with tab1:
         with st.form("master_data_form_tab1"):
            st.subheader("1. Unternehmensdaten")
            c1, c2 = st.columns(2)
            with c1:
                settings.company_name = st.text_input("Firmenname", settings.company_name)
                settings.address = st.text_input("Anschrift", settings.address)
            with c2:
                settings.currency = st.text_input("Währung", settings.currency)
                settings.vat_percent = st.number_input("MwSt (%)", 0.0, 100.0, settings.vat_percent)
    
            st.markdown("---")
            st.subheader("2. Stundenverrechnungssätze (Kalkulatorisch)")
            
            cw1, cw2, cw3 = st.columns(3)
            # Use distinct keys
            w_m = cw1.number_input("Unterhaltsreinigung (€/h)", value=settings.wage_maintenance)
            w_g = cw2.number_input("Glasreinigung (€/h)", value=settings.wage_glass)
            w_s = cw3.number_input("Sonderreinigung (€/h)", value=settings.wage_special)
            
            st.markdown("---")
            st.subheader("3. Zuschläge & Faktoren")
            cf1, cf2, cf3 = st.columns(3)
            with cf1:
                 lohnneben = st.number_input("Lohnnebenkosten (%)", value=settings.social_security_percent)
                 overhead = st.number_input("Gemeinkosten/Overhead (%)", value=settings.overhead_percent)
            with cf2:
                 mat = st.number_input("Materialkosten (%)", value=settings.material_percent)
                 equip = st.number_input("Gerätekosten (%)", value=settings.equipment_percent)
            with cf3:
                 margin = st.number_input("Ziel-Gewinnmarge (%)", value=settings.profit_margin_percent)
    
            if st.form_submit_button("Änderungen speichern", type="primary"):
                settings.wage_maintenance = w_m
                settings.wage_glass = w_g
                settings.wage_special = w_s
                
                settings.social_security_percent = lohnneben
                settings.overhead_percent = overhead
                settings.material_percent = mat
                settings.equipment_percent = equip
                settings.profit_margin_percent = margin
                
                db.commit()
                st.success("Stammdaten erfolgreich gespeichert!")
                st.rerun()

    # --- TAB 2: Reinigungsarten ---
    with tab2:
        st.info("Hier können Sie Reinigungsarten definieren (in Arbeit).")
        from ui.styles import get_css # Placeholder import or logic

    # --- TAB 4: Preisdatenbank ---
    with tab4:
        st.subheader("Übersicht Standard-Leistungspositionen (NRW/Herten Referenz)")
        st.caption("Diese Positionen basieren auf realen Leistungsverzeichnissen.")
        
        db_service = PriceDatabaseService()
        categories = db_service.get_database()
        
        for cat in categories:
            with st.expander(f"📂 {cat.name} (LB {cat.lb_code})", expanded=False):
                st.write(cat.description)
                data = []
                for p in cat.positions:
                   data.append({
                       "Nr.": p.pos_nr,
                       "Kurztext": p.kurztext,
                       "Ort": p.ort,
                       "Leistung (m²/h)": p.leistung_m2_h,
                       "Basis-EP (€)": p.ep_basis,
                       "Einheit": p.einheit
                   })
                if data:
                    st.dataframe(data, use_container_width=True)
