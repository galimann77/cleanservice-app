import streamlit as st
from sqlalchemy.orm import Session
from services.project_service import ProjectService
from models.project_data import Project

def render_result_view(db: Session):
    st.title("📊 Ergebnisse & Angebot")
    
    project_service = ProjectService(db)
    projects = project_service.get_projects()
    
    if not projects:
        st.info("Keine Projekte gefunden.")
        return
        
    proj_map = {p.name: p.id for p in projects}
    sel_proj_name = st.selectbox("Projekt wählen", list(proj_map.keys()))
    project = project_service.get_project(proj_map[sel_proj_name])
    
    if project.total_price_net == 0:
        st.warning("Dieses Projekt wurde noch nicht kalkuliert. Bitte zuerst im Raumbuch kalkulieren.")
        return

    # Key Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Gesamt (Netto/Monat)", f"{project.total_price_net:.2f} €")
    c2.metric("Stunden / Monat", f"{project.total_hours_monthly:.2f} h")
    c3.metric("Preis / m²", f"{(project.total_price_net / project.total_area):.2f} €" if project.total_area else "0 €")
    calc_hourly = (project.total_price_net / project.total_hours_monthly) if project.total_hours_monthly else 0
    c4.metric("Ø Verrechnungssatz", f"{calc_hourly:.2f} €/h")

    st.markdown("---")
    st.subheader("Angebotstext Vorschau")
    
    offer_text = f"""
    **ANGEBOT ZUR GEBÄUDEREINIGUNG**
    
    Projekt: {project.name}
    Kunde: {project.customer_name}
    
    Sehr geehrte Damen und Herren,
    
    gerne unterbreiten wir Ihnen folgendes Angebot für die Reinigung Ihres Objekts.
    
    **Leistungsübersicht:**
    Gesamtfläche: {project.total_area:.2f} m²
    
    **Monatliche Pauschale:**
    Netto: {project.total_price_net:.2f} €
    zzgl. 19% MwSt: {(project.total_price_net * 0.19):.2f} €
    **Brutto: {(project.total_price_net * 1.19):.2f} €**
    
    Im Preis enthalten sind alle Lohn-, Material- und Gerätekosten sowie die Anfahrt.
    Die Berechnung basiert auf den Tariflöhnen der Gebäudereiniger-Innung 2026.
    """
    
    st.text_area("Kopierbarer Text", offer_text, height=300)
    
    st.download_button("Angebot als Textdatei", offer_text, file_name=f"Angebot_{project.name}.txt")

    # --- Share Offer ---
    st.markdown("### Angebot teilen")
    if st.button("📤 Teilbaren Link erstellen", key="share_btn"):
        from services.offer_service import OfferService
        
        # Prepare Data Dict
        project_data = {
            "project_name": project.name,
            "customer_name": project.customer_name,
            "cost_summary": {
                "total_net_monthly": project.total_price_net,
                "total_gross_monthly": project.total_price_net * 1.19,
                "total_area": project.total_area
            },
            "offer_text": offer_text
        }
        
        # User ID from session or project
        user_id = st.session_state.get("username", "default_user")
        
        share_url = OfferService.create_shareable_offer(
            project_data,
            user_id
        )
        
        st.success("✅ Teilbarer Link erstellt!")
        st.code(share_url, language="text")
        st.caption("⚠️ Jeder mit diesem Link kann das Angebot sehen.")
