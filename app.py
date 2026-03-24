import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.init_db import init_database

# DB Init nur einmal pro Session
if 'db_initialized' not in st.session_state:
    try:
        init_database()
        st.session_state.db_initialized = True
    except Exception as e:
        st.error(f"❌ DB-Init fehlgeschlagen: {e}")
        st.stop()

from core.database import get_db, engine, Base
from ui.styles import get_css
from services.state_service import StateService

from services.draft_service import DraftService

# Ensure DB Tables exist (including drafts)
Base.metadata.create_all(bind=engine)

# Draft-Service available in session state
if 'draft_service' not in st.session_state:
    st.session_state.draft_service = DraftService

# ... imports ...
from ui.stammdaten_view import show_stammdaten
from ui.raumbuch_view import render_raumbuch_view
from ui.result_view import render_result_view
from ui.quick_calculation import render_quick_calculation
from ui.offer_creation_view import render_offer_creation_view
from ui.lv_view import render_lv_view
from services.calculation import CalculationService
from ui.construction_view import render_construction_cleaning_view
from services.lv_service import LVProject
from ui.dashboard_view import show_dashboard

# Load Custom CSS
st.markdown(get_css(), unsafe_allow_html=True)

if 'current_lv' not in st.session_state:
    # Try loading Draft
    db = next(get_db())
    draft_data = StateService.load_latest_draft(db, "default_user")
    if draft_data:
        # Reconstruct LVProject from JSON 
        # (Assuming LVProject has from_dict or simple init, we might need to adjust LVProject model)
        # For now, let's just say we found it. We need to implement serialization in LVProject properly.
        # Fallback to new if complex.
        try:
             # Basic reconstruction for now
             st.session_state.current_lv = LVProject(**draft_data)
             st.toast("Letzter Entwurf geladen!", icon="📂")
        except:
             st.session_state.current_lv = LVProject(name="Unbenannt", date="2026-02-08")
    else:
        st.session_state.current_lv = LVProject(name="Unbenannt", date="2026-02-08")

# --- Authentication ---
from auth.authenticator import show_login, init_authenticator

# Initialize Session State for Auth
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.title("🔐 CLEANSERVICE Login")
        if show_login():
            st.rerun()
    st.stop()

# Ab hier: Nur für eingeloggte User
authenticator = init_authenticator()

# Sidebar Logout
with st.sidebar:
    st.write(f"👤 {st.session_state.get('user_name', 'User')}")
    authenticator.logout('Logout', 'main')

# --- Sidebar ---
st.sidebar.markdown("""
    <div class="sidebar-header">
        <div class="logo-box">CS</div>
        <div style="display: flex; flex-direction: column;">
            <h2 style="margin:0; font-size: 1.3rem; line-height: 1.2; color: #f8fafc !important;">CLEANSERVICE</h2>
            <span style="color: #94a3b8; font-size: 0.9rem; font-weight: 500;">Kalkulator 5.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
st.sidebar.markdown("---")

st.sidebar.title("Navigation")

# Session State for Navigation
if 'app_mode' not in st.session_state:
    st.session_state['app_mode'] = 'Dashboard'
    
# Callback to handle sidebar changes
def on_nav_change():
    st.session_state['app_mode'] = st.session_state['nav_selection']

# Sidebar Radio with key and callback
app_mode = st.sidebar.radio("Menü:",
    ["Dashboard", "Schnellkalkulation", "Baureinigung (VOB)", "Universal-Angebot 🆕", "Leistungsverzeichnis (LV)", "Raumbuch & Kalkulation", "Ergebnisse & Angebot", "Stammdaten"],
    key="nav_selection",
    on_change=on_nav_change,
    index=0
)

st.sidebar.markdown("---")
# ...

service = CalculationService()
db = next(get_db())

# Dispatcher based on session state
current_mode = st.session_state['app_mode']

if current_mode == "Dashboard":
    show_dashboard()
elif current_mode == "Schnellkalkulation":
    from ui.express_view import show_express_calculator
    show_express_calculator()
elif current_mode == "Baureinigung (VOB)":
    render_construction_cleaning_view(db)
elif current_mode == "Universal-Angebot 🆕":
     render_offer_creation_view(db)
elif current_mode == "Leistungsverzeichnis (LV)":
    render_lv_view(db)
elif current_mode == "Raumbuch & Kalkulation":
    render_raumbuch_view(db)
elif current_mode == "Ergebnisse & Angebot":
    render_result_view(db)
elif current_mode == "Stammdaten":
    show_stammdaten()
