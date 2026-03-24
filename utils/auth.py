import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

def init_auth():
    # Hardcoded fallback credentials for demo
    # In production, load from yaml or DB
    credentials = {
        'usernames': {
            'admin': {
                'name': 'Admin User',
                'password': 'abc' # Will be hashed below if needed, but stauth expects hashed
            },
            'demo': {
                'name': 'Demo User',
                'password': '123' 
            }
        }
    }
    
    # Pre-hash simple passwords for the demo
    # In real world, use: stauth.Hasher(['your_password']).generate()
    hashed_passwords = stauth.Hasher(['abc', '123']).generate()
    credentials['usernames']['admin']['password'] = hashed_passwords[0]
    credentials['usernames']['demo']['password'] = hashed_passwords[1]

    authenticator = stauth.Authenticate(
        credentials,
        'cleanservice_app',
        'auth_key_12345',
        cookie_expiry_days=30
    )
    
    return authenticator

def require_auth():
    authenticator = init_auth()
    # Login widget
    try:
        # Correct call based on introspection: login(self, location, ...)
        # There is NO form_name argument in this version (0.3.3) apparently?
        # varnames: ('self', 'location', 'max_concurrent_users', 'max_login_attempts',
        #            'fields', 'captcha', 'clear_on_submit', 'key', 'callback', 'sleep_time', ...)
        name, authentication_status, username = authenticator.login('main')
    except Exception as e:
        st.error(f"Auth Error: {e}")
        st.stop()
    
    if authentication_status:
        # st.write(f'Welcome *{name}*')
        st.session_state["authentication_status"] = True
        st.session_state["username"] = username
        return True, authenticator
    elif authentication_status == False:
        st.error('Username/password is incorrect')
        st.stop()
        return False, None
    elif authentication_status == None:
        st.warning('Please enter your username and password')
        st.stop()
        return False, None
