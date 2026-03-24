import streamlit as st
from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@st.cache_resource
def get_gemini_client_instance():
    """Cached singleton for GenAI Client."""
    # Priority: Env Var > Secrets
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        try:
            if "GOOGLE_API_KEY" in st.secrets:
                api_key = st.secrets["GOOGLE_API_KEY"]
        except:
            pass
            
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

@st.cache_data(ttl=3600, show_spinner=False)
def analyze_building_text_cached(text: str) -> dict:
    """Cached AI Analysis for building text."""
    client = get_gemini_client_instance()
    if not client:
        return {"error": "Google API Key missing."}

    prompt = f"""
    You are an expert Building Cleaning Calculator Assistant.
    Analyze the following text description of a building project and extract a list of rooms and their cleaning requirements.
    
    Text: "{text}"
    
    Return ONLY a raw JSON object (no markdown formatting) with the following structure:
    {{
        "project_name": "Suggested Project Name",
        "rooms": [
            {{
                "name": "Room Name (e.g. Office 101)",
                "type": "office_std" | "office_full" | "sanitary" | "corridor" | "glass_window", 
                "area": float (estimate if not specified, e.g. Office=20, WC=10),
                "service_id": "office_std" | "office_full" | "sanitary" | "corridor",
                "frequency": int (250=5x/week, 52=1x/week, 12=monthly)
            }}
        ]
    }}
    
    Valid Service/Room Types:
    - office_std (Standard Office)
    - office_full (Crowded Office)
    - sanitary (WC/Kitchen)
    - corridor (Flur/Treppe)
    - glass_window (Fenster)
    
    Be realistic with area estimates if not provided.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        clean_text = response.text.strip()
        return json.loads(clean_text)
    except Exception as e:
        return {"error": str(e)}

class GeminiClient:
    def __init__(self):
        self.client = get_gemini_client_instance()

    def analyze_building_text(self, text: str) -> dict:
        # Wrapper to use cached function
        return analyze_building_text_cached(text)

    def check_plausibility(self, project_summary: str) -> str:
        """
        Checks the plausibility of a calculation summary.
        Currently not cached as it might be context specific/interactive.
        """
        if not self.client:
             return "AI not configured."
             
        prompt = f"""
        Analyze this cleaning calculation for plausibility:
        {project_summary}
        
        Check for:
        1. Unrealistic performance values (m²/h)
        2. Pricing anomalies (too low/high)
        3. Missing common areas (e.g. office but no WC)
        
        Reply in German, short and professional.
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Fehler bei Analyse: {str(e)}"
