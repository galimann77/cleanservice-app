import streamlit as st
from sqlalchemy.orm import Session
from services.project_service import ProjectService
from services.calculation_engine import CalculationEngine
from services.gemini_client import GeminiClient
from models.master_data import ServiceCategory, ServiceType
from models.project_data import Project, Room, CleaningTask
import json
from utils.file_handling import save_uploaded_files

def render_raumbuch_view(db: Session):
    st.title("📐 Raumbuch & Kalkulation")
    
    project_service = ProjectService(db)
    engine = CalculationEngine(db)
    
    # 1. Project Selection
    projects = project_service.get_projects()
    project_options = {f"{p.name} ({p.customer_name})": p.id for p in projects}
    
    col_sel, col_new = st.columns([3, 1])
    with col_sel:
        search_proj = st.selectbox("Projekt auswählen", options=list(project_options.keys()), index=0 if projects else None)
    
    with col_new:
        if st.button("➕ Neues Projekt"):
            st.session_state.show_new_project_form = True

    if st.session_state.get("show_new_project_form"):
        with st.form("new_proj"):
            new_name = st.text_input("Projektname")
            new_cust = st.text_input("Kunde")
            if st.form_submit_button("Anlegen"):
                project_service.create_project(new_name, new_cust)
                st.session_state.show_new_project_form = False
                st.rerun()

    if not search_proj:
        st.info("Bitte wählen oder erstellen Sie ein Projekt.")
        return

    selected_project_id = project_options[search_proj]
    project = project_service.get_project(selected_project_id)

    # --- AI Import Section ---
    st.markdown("---")
    with st.expander("🤖 AI-Import: Raumbuch aus Beschreibung generieren", expanded=False):
        st.caption("Beschreiben Sie das Objekt (z.B. 'Büroetage mit 10 Büros a 20qm, 2 WCs, 1 Küche')")
        ai_text = st.text_area("Objektbeschreibung", height=100)
        
        if st.button("Analysieren & Generieren", type="secondary"):
            if not ai_text:
                st.warning("Bitte Text eingeben.")
            else:
                try:
                    client = GeminiClient()
                    if not client.client:
                        st.error("Google API Key fehlt. Bitte .env prüfen.")
                    else:
                        with st.spinner("Gemini analysiert das Gebäude..."):
                            data = client.analyze_building_text(ai_text)
                        
                        if "error" in data:
                            st.error(f"Fehler: {data['error']}")
                        else:
                            # Process Result
                            st.success(f"Analyse erfolgreich! {len(data.get('rooms', []))} Räume gefunden.")
                            
                            # Preview
                            st.json(data)
                            
                            if st.button("Daten übernehmen?", key="confirm_ai_import"):
                                # Import Logic
                                cnt = 0
                                for r_data in data.get("rooms", []):
                                    # Map AI type to our IDs (simple mapping for now)
                                    # In a real app, we'd make this robust
                                    room = project_service.add_room(project.id, r_data.get("name", "Raum"), r_data.get("area", 10.0), r_data.get("type", "Standard"))
                                    
                                    # Add Task
                                    srv_id = r_data.get("service_id", "office_std")
                                    # Check if service exists, else valid defaults
                                    # ... implementation detail ...
                                    project_service.add_task(room.id, srv_id, r_data.get("frequency", 250))
                                    cnt += 1
                                
                                st.success(f"{cnt} Räume importiert!")
                                st.rerun()
                                
                except Exception as e:
                    st.error(f"Systemfehler: {e}")


    # 2. Add Room & Task (Inline Form for speed)
    st.markdown("---")
    st.subheader("Raum manuell hinzufügen")
    
    with st.form("add_room_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([2, 1, 2, 1])
        r_name = c1.text_input("Raumbezeichnung (z.B. Büro 101)")
        r_area = c2.number_input("Fläche (m²)", min_value=1.0, value=20.0)
        
        # Service Selection
        # Group by Category? For now simple list
        services = db.query(ServiceType).all()
        service_opts = {f"{s.name} ({s.performance_avg} m²/h)": s.id for s in services}
        r_service_label = c3.selectbox("Leistung", list(service_opts.keys()))
        r_freq = c4.number_input("Turnus (x/Jahr)", value=250, help="250 = 5x/Woche, 52 = 1x/Woche")
        
        if st.form_submit_button("Raum & Leistung hinzufügen"):
            # Creates Room AND Task in one go for speed
            # Determine Room Type from Service? Optional.
            room = project_service.add_room(project.id, r_name, r_area, "Standard")
            project_service.add_task(room.id, service_opts[r_service_label], r_freq)
            st.success("Hinzugefügt!")
            st.rerun()

    # 3. Raumbuch Table
    st.markdown("---")
    st.subheader(f"Raumbuch: {project.name}")
    
    if not project.rooms:
        st.info("Noch keine Räume angelegt.")
    else:
        # Display as expansive list or data editor
        total_area = sum(r.area_sqm for r in project.rooms)
        st.caption(f"Gesamtfläche: {total_area:.2f} m² | {len(project.rooms)} Räume")
        
        for room in project.rooms:
            with st.expander(f"{room.name} ({room.area_sqm} m²)"):
                # List Tasks
                for task in room.tasks:
                    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                    c1.markdown(f"**{task.service_type.name}**")
                    c2.text(f"{task.frequency_per_year}x / Jahr")
                    
                    # Calculated values (if present)
                    perf = task.performance_used or task.service_type.performance_avg
                    c3.caption(f"Leistung: {perf} m²/h")
                    
                    if c4.button("🗑️", key=f"del_task_{task.id}"):
                        project_service.delete_task(task.id)
                        st.rerun()
                
                # --- Photos & AI Vision ---
                st.markdown("---")
                c_ph1, c_ph2 = st.columns([3, 1])
                with c_ph1:
                    new_photos = st.file_uploader("📷 Fotos hochladen (für AI-Analyse)", accept_multiple_files=True, key=f"up_{room.id}", type=["png", "jpg", "jpeg"])
                
                # Show existing
                try:
                    existing_photos = json.loads(room.photos_json) if room.photos_json else []
                except:
                    existing_photos = []

                if existing_photos:
                    st.image(existing_photos, width=100, caption=[p.split('/')[-1] for p in existing_photos])
                
                if new_photos:
                    if st.button("Speichern & Analysieren", key=f"btn_upload_{room.id}"):
                        saved_paths = save_uploaded_files(new_photos, project.id, room.id)
                        all_photos = existing_photos + saved_paths
                        room.photos_json = json.dumps(all_photos)
                        
                        # Vision AI Stub
                        from services.vision_service import analyze_room_photos
                        # ai = AIService() # Old
                        analysis = analyze_room_photos(saved_paths)
                        if "analysis" in analysis:
                            st.toast(f"AI: {analysis['analysis']}", icon="🤖")
                        
                        db.commit()
                        st.success("Fotos gespeichert!")
                        st.rerun()
                
                if st.button("Raum löschen", key=f"del_room_{room.id}"):
                    project_service.delete_room(room.id)
                    st.rerun()

    # 4. Action Bar
    st.markdown("### Aktionen")
    if st.button("🚀 Projekt Kalkulieren & Speichern", type="primary"):
        updated_proj = engine.calculate_project(project)
        db.commit()
        
        # Auto-Save Draft
        if "draft_service" in st.session_state:
            # Create a simple dict representation or use pydantic dump if available
            # For now, just a basic stub to prove integration as we don't have full serialization logic yet
            draft_data = {
                "id": project.id,
                "name": project.name,
                "total": updated_proj.total_price_net,
                "rooms": len(project.rooms)
            }
            try:
                st.session_state.draft_service.auto_save_draft(
                    db, 
                    st.session_state.get("username", "default_user"), 
                    project.name, 
                    "raumbuch", 
                    draft_data
                )
                st.toast("Entwurf automatisch gespeichert", icon="💾")
            except Exception as e:
                print(f"Draft save failed: {e}")

        st.success("Kalkulation erfolgreich!")
        st.metric("Neuer Monatspreis (Netto)", f"{updated_proj.total_price_net:.2f} €")
