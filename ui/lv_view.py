import streamlit as st
import pandas as pd
from services.lv_service import LVGenerator, LVProject, LVPosition
from services.state_service import StateService
from sqlalchemy.orm import Session
import io

# Store current LV in Session State to act as a "Cart"
if "current_lv" not in st.session_state:
    st.session_state.current_lv = LVProject(name="Neues LV", date="2026-02-08")

def render_lv_view(db: Session):
    st.title("📑 Leistungsverzeichnis (LV)")
    st.caption("Erstellen und exportieren Sie VOB-konforme Leistungsverzeichnisse. (Automatische Speicherung aktiv ✅)")
    
    lv = st.session_state.current_lv
    
    # --- Toolbar ---
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.subheader(f"Projekt: {lv.name}")
    with c2:
        if st.button("🗑️ LV Leeren"):
            st.session_state.current_lv = LVProject(name="Neues LV", date="2026-02-08")
            StateService.save_draft(db, "default_user", "Entwurf", st.session_state.current_lv.to_dict())
            st.rerun()
    with c3:
        if st.button("💾 Speichern"):
             StateService.save_draft(db, "default_user", "Entwurf", st.session_state.current_lv.to_dict())
             st.toast("Entwurf gespeichert!")
 
    # --- LV Table ---
    if not lv.positions:
        st.info("Das Leistungsverzeichnis ist leer. Importieren Sie Positionen aus der Kalkulation.")
    else:
        # Prepare Data for Table
        data = []
        for p in lv.positions:
            data.append({
                "OZ": p.oz,
                "Kurztext": p.kurztext,
                "Menge": p.menge,
                "Einheit": p.einheit,
                "EP (€)": f"{p.ep:.2f}",
                "GP (€)": f"{p.gp:.2f}"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # --- Totals ---
        total = lv.get_total_net()
        st.markdown(f"### Gesamtsumme (Netto): :green[{total:.2f} €]")
        
        # --- Detail View (Langtext) ---
        st.markdown("---")
        st.subheader("🔍 Positions-Details (Langtext)")
        
        selected_oz = st.selectbox("Position zur Ansicht wählen:", options=[p.oz for p in lv.positions])
        
        if selected_oz:
            pos = next((p for p in lv.positions if p.oz == selected_oz), None)
            if pos:
                st.markdown(f"**{pos.kurztext}**")
                st.text_area("Langtext (Ausschreibungstext)", pos.langtext, height=150)
                
    # --- Export ---
    st.markdown("---")
    st.subheader("📤 Export & Ausgabe")
    
    col_ex1, col_ex2 = st.columns(2)
    
    with col_ex1:
        # Excel Export logic
        if st.button("Excel-Export (.xlsx)"):
            # Mock Export for now (CSV actually)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Datei herunterladen",
                csv,
                "leistungsverzeichnis.csv",
                "text/csv",
                key='download-csv'
            )
            
    with col_ex2:
         st.markdown("GAEB-Export (XML) ist in Vorbereitung.")

def add_to_lv(items, db: Session, attributes=None):
    """Helper to add items from other views to Global LV."""
    if "current_lv" not in st.session_state:
         st.session_state.current_lv = LVProject(name="Neues LV", date="2026-02-08")
         
    lv = st.session_state.current_lv
    generator = LVGenerator() # Was creating new instance
    
    start_index = len(lv.positions) + 1
    
    for i, item in enumerate(items):
        pos = LVGenerator.create_position_from_calc(item, start_index + i, attributes) # static method call fixed
        lv.positions.append(pos)
        
    StateService.save_draft(db, "default_user", "Entwurf", lv.to_dict())
    st.toast(f"{len(items)} Positionen zum LV hinzugefügt & gespeichert!")
