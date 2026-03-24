import streamlit as st
import pandas as pd
from services.vob_structure import VOBStructureService
from services.lv_service import LVProject, LVPosition, LVGenerator
from services.state_service import StateService
from sqlalchemy.orm import Session

def render_construction_cleaning_view(db: Session):
    st.title("🏗️ Baureinigung & VOB Ausschreibung")
    st.caption("Kalkulation für Baugrob- und Baufeinreinigung nach VOB-Struktur (Referenz-LV).")
    
    vob_service = VOBStructureService()

    # --- 1. PROJEKTDATEN ---
    with st.expander("📋 Projekt & Bauphase", expanded=True):
        c1, c2 = st.columns(2)
        projectName = c1.text_input("Projektname", "Umbau/Sanierung FBS Datteln")
        bauphase = c2.selectbox(
            "Bauphase / Reinigungsart", 
            ["Baugrobreinigung (Zwischenreinigung)", "Baufeinreinigung (Schlussreinigung)", "Kombination (Grob & Fein)"]
        )
    
    # --- 2. LEISTUNGSERFASSUNG ---
    st.subheader("Flächen & Bauteile (Leistungsverzeichnis)")
    
    all_services = vob_service.get_construction_services()
    displayed_services = []

    # Filter Logic
    is_grob = "Baugrob" in bauphase
    is_fein = "Baufein" in bauphase
    is_kombi = "Kombination" in bauphase
    
    # Logic: 
    # Grob -> only is_grob items
    # Fein -> only is_fein items
    # Kombi -> All items
    
    if is_kombi:
        displayed_services = all_services
    elif is_grob:
        displayed_services = [s for s in all_services if s.is_grob]
    elif is_fein:
        displayed_services = [s for s in all_services if s.is_fein]

    # --- Input Mask (Tabular Style) ---
    
    # Header
    h1, h2, h3, h4 = st.columns([3, 2, 2, 1])
    h1.markdown("**Leistungsbezeichnung**")
    h2.markdown("**Ort / Bereich**")
    h3.markdown("**Menge**")
    h4.markdown("**Einh.**")
    
    # State for Inputs
    inputs = {}
    
    for s in displayed_services:
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
        c1.write(f"{s.name}")
        c2.caption(s.location_default)
        
        # Menge Input
        qty = c3.number_input(
            f"qty_{s.id}", 
            min_value=0.0, 
            value=0.0, 
            step=10.0 if s.unit == "m²" else 1.0, 
            key=f"input_{s.id}",
            label_visibility="collapsed"
        )
        c4.write(s.unit)
        
        inputs[s.id] = {
            "service": s,
            "qty": qty
        }
        
    st.markdown("---")

    # --- 3. KALKULATION & LV ERSTELLUNG ---
    
    if st.button("🚀 Kalkulation erstellen & LV generieren", type="primary"):
        st.spinner("Berechne Preise und erstelle Leistungsverzeichnis...")
        
        # 1. Collect Active Items
        active_items = []
        for sid, data in inputs.items():
            if data["qty"] > 0:
                active_items.append(data)
        
        if not active_items:
            st.error("Bitte geben Sie Mengen > 0 ein, um eine Kalkulation zu erstellen.")
            return

        # 2. Perform Calculation
        lv_positions = []
        wage_rates = vob_service.get_wage_rates()
        surcharges = vob_service.get_surcharges()
        
        # Total Surcharge Factor Calculation
        # Costs = Lohn + Lohnneben(80%) + Gemein(15%) + Material(5%) + Geräte(2%) + Gewinn(25%)
        # Basis Lohn = 1.0
        # Personalzusatzkosten = 1.0 * (1 + 0.80) = 1.80 (Lohnkosten voll)
        # Material/Geräte sind meist aufschlagsbasiert auf Lohn oder separat. 
        # Simplified Surcharge Logic based on Prompt:
        # "Addiere Zuschläge..." - usually strictly distinct, but let's do a bottom-up price build.
        
        # Factor for Calculation:
        # Wage * 1.80 (Lohnkosten)
        # + Material share? (Let's assume material is incl in hourly rate logic or add 5% on top)
        # Let's use a Multiplier approach common in cleaning:
        # Cost = Wage * (1 + LNK + GK + Mat + Dev + Profit)
        # Sum of factors = 0.8 + 0.15 + 0.05 + 0.02 + 0.25 = 1.27
        # Total Factor = 1 + 1.27 = 2.27
        
        total_factor = 1.0 + sum(surcharges.values())
        
        total_net = 0.0
        total_sqm = 0.0
        total_hours = 0.0
        
        for idx, item in enumerate(active_items):
            s = item["service"]
            q = item["qty"]
            
            # Determine Wage
            wage = wage_rates.get(s.wage_type, 18.40)
            
            # Calc Time
            if s.unit == "Psch":
                # Special Case: Pauschal needs explicit price input or assumption.
                # For Reference LV "01.1", let's assume a fixed price input or calculate logic?
                # Prompt says: "Baugrobreinigung Pauschal... EP 450,00".
                # For this demo, let's treat Psch as 1.0 amount * Manual Rate or Fixed Calc.
                # We will define a default hours for Psch or assume 450€ base.
                is_psch = True
                calc_price = 450.00 * q # Hardcoded logic for demo "01.1" usually needs customization
                perf = 0
                hours = 10.0 # Assumed
            else:
                is_psch = False
                perf = s.performance
                if perf > 0:
                    hours = q / perf
                else:
                    hours = 0
                
                # Cost Build-up
                base_cost = hours * wage
                calc_price = base_cost * total_factor
            
            # Result Values
            ep = calc_price / q if q > 0 else 0
            gp = calc_price
            
            total_net += gp
            if s.unit == "m²": total_sqm += q
            total_hours += hours
            
            # Create LV Obj
            pos = LVPosition(
                oz=s.id,
                titel="01 Baugrobreinigung" if s.is_grob else "02 Bauendreinigung",
                kurztext=s.name,
                langtext=f"{s.description} Ort: {s.location_default}.",
                menge=q,
                einheit=s.unit,
                ep=ep,
                gp=gp,
                stlb_lb="033"
            )
            lv_positions.append(pos)

        # 3. Create Project & Title Structure (Grouping)
        project = LVProject(name=projectName, date=pd.Timestamp.now().strftime("%d.%m.%Y"))
        project.positions = lv_positions
        
        # Save to Session
        st.session_state.current_lv = project
        StateService.save_draft(db, "default_user", "Entwurf", project.to_dict())
        
        # 4. Result Display
        st.success("✅ Kalkulation erfolgreich erstellt!")
        
        st.markdown(f"""
        <div style="background-color: #f0f9ff; padding: 20px; border-radius: 8px; border: 1px solid #bae6fd;">
            <h4>Zusammenfassung</h4>
            <ul>
                <li><b>Positionen:</b> {len(active_items)}</li>
                <li><b>Gesamtfläche:</b> {total_sqm:.2f} m²</li>
                <li><b>Geschätzter Zeitbedarf:</b> {total_hours:.2f} h</li>
                <li><b>Gesamtpreis Netto:</b> {total_net:,.2f} €</li>
                <li><b>MwSt (19%):</b> {total_net*0.19:,.2f} €</li>
                <li><b>Gesamtpreis Brutto:</b> {total_net*1.19:,.2f} €</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("📋 Zum Leistungsverzeichnis"):
            # Switch Page Hack via Session State or just guidance
            st.session_state["nav_selection"] = "Leistungsverzeichnis (LV)" # Assuming this key controls nav
            st.rerun() # Might need to adjust app.py to listen to this
            
        # Optional: Direct Docx Offer

