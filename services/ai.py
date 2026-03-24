import google.generativeai as genai
import json
import os
from typing import Optional, Dict, Any
from config import Config
import streamlit as st

class AIService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.get_gemini_key()
        self.model = self._get_model(self.api_key)

    @staticmethod
    @st.cache_resource(show_spinner=False)
    def _get_model(api_key: Optional[str]):
        if api_key:
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-2.0-flash')
        return None

    def analyze_description(self, description: str, available_types: list) -> Dict[str, Any]:
        if not self.model:
            return {"error": "API Key missing"}

        types_str = ", ".join([t.name for t in available_types])
        
        prompt = f"""
        Du bist ein Experte für Gebäudereinigung. Analysiere die folgende Objektbeschreibung und extrahiere Parameter für eine Kalkulation.
        
        Beschreibung: "{description}"
        
        Verfügbare Reinigungsarten im System: {types_str}
        
        Bitte antworte ausschließlich im JSON-Format mit folgenden Feldern:
        - "suggested_cleaning_type": (Name einer der verfügbaren Reinigungsarten, die am besten passt)
        - "area_sqm": (Geschätzte Fläche als Zahl, falls genannt oder schätzbar, sonst null)
        - "dirt_level": ("leicht", "normal", "stark", "extrem")
        - "addons": (Liste von passenden Zusatzleistungen wie "Fugen reinigen", "Imprägnieren", "Fest verfugen" falls erwähnt)
        - "reasoning": (Kurze Begründung für die Wahl, max 2 Sätze)
        - "difficulty_factor": (Schätzung 1.0 bis 2.0 für Erschwernisse wie Zugang etc.)

        JSON:
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean up potential markdown code blocks
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            return {"error": str(e)}

    def analyze_room_photos(self, photos: list) -> dict:
        """
        Placeholder for Vision AI.
        Currently just returns a mock analysis.
        """
        if not photos:
            return {"error": "No photos provided"}
        
        # Mock Response
        return {
            "analysis": "Vision AI Stub: Raum scheint ein Büro zu sein (Erkannt: Schreibtisch, Fenster).",
            "suggested_dirt_level": "normal"
        }
