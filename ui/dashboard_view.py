import streamlit as st
from core.database import get_db
from models.draft_model import ProjectDraft

def show_dashboard():
    st.title("📊 Dashboard")
    st.caption("Übersicht Ihrer Projekte")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Offene Angebote", "7", delta="2")
    col2.metric("Ø Gewinnmarge", "23%", delta="-2%")
    col3.metric("Erfolgsquote", "68%", delta="5%")
    col4.metric("Ø Angebotswert", "12.400 €")
    
    st.divider()
    st.subheader("📁 Zuletzt bearbeitet")
    
    db = next(get_db())
    try:
        # Use simple session state for compatibility if passed as arg, 
        # but here we use get_db() directly as requested.
        user_id = st.session_state.get("username", "default_user")
        
        drafts = db.query(ProjectDraft).filter_by(
            user_id=user_id
        ).order_by(ProjectDraft.updated_at.desc()).limit(5).all()
        
        if drafts:
            for draft in drafts:
                with st.container():
                    col_a, col_b, col_c = st.columns([3, 2, 1])
                    col_a.write(f"**{draft.project_name or 'Unbenannt'}**")
                    col_b.caption(f"🕒 {draft.updated_at.strftime('%d.%m %H:%M')}")
                    if col_c.button("Öffnen", key=f"open_{draft.id}"):
                        st.session_state.current_draft_id = draft.id
                        st.session_state['app_mode'] = "Raumbuch & Kalkulation"
                        st.rerun()
        else:
            st.info("Noch keine Projekte")
    finally:
        db.close()
    
    st.divider()
    st.subheader("⚡ Schnellzugriff")
    col_x, col_y, col_z = st.columns(3)
    
    if col_x.button("➕ Neue Kalkulation", use_container_width=True, type="primary"):
        st.session_state['app_mode'] = "Stammdaten"
        st.rerun()
    if col_y.button("⚡ Express-Rechner", use_container_width=True):
        st.session_state['app_mode'] = "Schnellkalkulation"
        st.rerun()
    if col_z.button("📋 Leistungsverzeichnis", use_container_width=True):
        st.session_state['app_mode'] = "Leistungsverzeichnis (LV)"
        st.rerun()
