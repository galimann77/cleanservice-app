import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

def load_auth_config():
    config_path = os.path.join(os.path.dirname(__file__), 'auth_config.yaml')
    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def init_authenticator():
    config = load_auth_config()
    
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
    return authenticator

def show_login():
    """
    Zeigt Login-Maske und gibt auth_status zurück.
    """
    authenticator = init_authenticator()
    
    try:
        # Check version signature. v0.3.3 takes 'form_name', 'location' ? 
        # Prompt says: login('Login', 'main')
        # We'll use the prompt's signature.
        name, authentication_status, username = authenticator.login('main')
    except Exception as e:
        # Fallback if signature mismatch
        st.error(f"Auth Error: {e}")
        return False
    
    if authentication_status:
        st.session_state.authenticated = True
        st.session_state.user_id = username
        st.session_state.username = username # Compatibility
        st.session_state.user_name = name
        return True
    elif authentication_status == False:
        st.error('❌ Benutzername/Passwort falsch')
        return False
    elif authentication_status == None:
        st.warning('Bitte einloggen')
        return False
    return False
