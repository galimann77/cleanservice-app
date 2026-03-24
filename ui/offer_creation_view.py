import streamlit as st
import pandas as pd
from services.price_db_service import PriceDatabaseService
from services.calculation import CalculationService
from services.lv_service import LVPosition
from ui.lv_view import add_to_lv
from services.state_service import StateService
from sqlalchemy.orm import Session

def render_offer_creation_view(db: Session):
    st.title("📝 Universal-Angebotserstellung")
    st.caption("Erstellen Sie Angebote für alle Reinigungsarten basierend auf der Preisdatenbank.")

    db_service = PriceDatabaseService()
    categories = db_service.get_database()

    # --- 1. Position Selection ---
    st.subheader("1. Leistung auswählen")
    
    c1, c2 = st.columns(2)
    selected_cat_name = c1.selectbox("Kategorie", [c.name for c in categories])
    selected_cat = next(c for c in categories if c.name == selected_cat_name)
    
    selected_pos_text = c2.selectbox("Position", [p.kurztext for p in selected_cat.positions])
    pos = next(p for p in selected_cat.positions if p.kurztext == selected_pos_text)

    # --- 2. Configuration ---
    st.subheader("2. Details & Mengen")
    
    # Removed st.form to ensure immediate state updates for Menge
    col_A, col_B = st.columns(2)
    
    with col_A:
        st.markdown(f"**{pos.kurztext}**")
        st.caption(pos.langtext)
        st.text_input("Ort / Bereich", value=pos.ort, key="custom_ort")
        
    with col_B:
         # Use session state to persist manual changes to Menge if needed, 
        # or just rely on the widget state correctly. 
        # The issue might be that key wasn't unique or form submission behavior.
        # Let's give it a key.
        menge = st.number_input(f"Menge ({pos.einheit})", min_value=1.0, value=100.0, step=10.0, key=f"menge_{pos.pos_nr}")
        
        # Turnus Selection
        if pos.turnus_faktoren:
            turnus = st.selectbox("Turnus / Häufigkeit", list(pos.turnus_faktoren.keys()), key=f"turnus_{pos.pos_nr}")
            turnus_factor = pos.turnus_faktoren[turnus]
        else:
            turnus = "Standard"
            turnus_factor = 1.0
        
        # Price Calculation
        # Basis Price * Turnus Factor
        calc_ep = pos.ep_basis * turnus_factor
        
        st.metric("Kalkulierter EP (Basis)", f"{calc_ep:.2f} €", help=f"Basis: {pos.ep_basis} x Faktor {turnus_factor}")
        
        # Manual Override
        final_ep = st.number_input("Endgültiger EP (Netto)", value=calc_ep, step=0.10, key=f"ep_{pos.pos_nr}")
        
        # Plausibility Check
        from services.calculation import get_calculation_service_v2
        db_service_calc = get_calculation_service_v2() # Or inject if available
        check_result = db_service_calc.check_plausibility(pos.pos_nr, final_ep, mode="price")
        
        if not check_result["is_plausible"]:
            if check_result["level"] == "warning":
                st.warning(check_result["message"])
            elif check_result["level"] == "error":
                st.error(check_result["message"])
            elif check_result["level"] == "info":
                st.info(check_result["message"])
        else:
            st.caption(f"✅ {check_result['message']}")
        
    submitted = st.button("➕ Zum Angebot (LV) hinzufügen", type="primary")
    
    if submitted:
        # Create LV Position
        # We map the DB position to the LV Position structure
        
        # Dynamic Longtext if needed, or stick to DB text
        full_text = f"{pos.langtext}\n\nAusführung: {turnus}."
        
        # Create pseudo-calc item for add_to_lv helper or create manually
        new_pos = LVPosition(
            oz="auto", # will be set by LV logic
            titel=selected_cat.name,
            kurztext=f"{pos.kurztext} ({turnus})",
            langtext=full_text,
            menge=menge, # Use the variable from the widget
            einheit=pos.einheit,
            ep=final_ep,
            gp=final_ep * menge,
            stlb_lb=selected_cat.lb_code
        )
        
        # Add to Session Logic
        if "current_lv" not in st.session_state:
            # Initialize LV if missing (should be done in app start but failsafe here)
            from services.lv_service import LVProject
            st.session_state.current_lv = LVProject(name="Unbenannt", date="2026-02-08")

        current_lv = st.session_state.current_lv
        # Auto-Numbering
        idx = len(current_lv.positions) + 1
        new_pos.oz = f"{idx:02d}.00" 
        current_lv.positions.append(new_pos)
        StateService.save_draft(db, "default_user", "Entwurf", current_lv.to_dict())
        st.success(f"Position '{new_pos.kurztext}' mit Menge {menge} {pos.einheit} hinzugefügt! (Gespeichert)")

    # --- 3. Preview ---
    if "current_lv" in st.session_state and st.session_state.current_lv.positions:
        st.markdown("---")
        st.subheader("Aktuelle Positionen im Angebot")
        df = pd.DataFrame([{
            "Kurztext": p.kurztext,
            "Menge": p.menge,
            "EP": p.ep,
            "GP": p.gp
        } for p in st.session_state.current_lv.positions])
        st.dataframe(df)
