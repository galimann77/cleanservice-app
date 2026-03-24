import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "cleaning_data.json")
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(os.path.dirname(__file__), 'data', 'cleancalculator.db')}"
    )
    
    # Postgres-specific Settings
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_ECHO = os.getenv("DB_ECHO", "False").lower() == "true"
    
    @staticmethod
    def is_sqlite():
        return Config.DATABASE_URL.startswith("sqlite")

    @staticmethod
    def get_gemini_key():
        # 1. Try Environment Variable (Local .env)
        if Config.GEMINI_API_KEY:
            return Config.GEMINI_API_KEY
        
        # 2. Try Streamlit Secrets (Cloud)
        try:
            import streamlit as st
            if "GEMINI_API_KEY" in st.secrets:
                return st.secrets["GEMINI_API_KEY"]
        except:
            pass
            
        return None
