# CLEANSERVICE Kalkulator 5.0

Professionelle B2B SaaS Anwendung für Gebäudereiniger.

## Features 5.0
- **Kalkulation**: Präzise Berechnung nach qm, Leistungswerten und Tariflohn.
- **Express-Modus**: Sofort-Preisindikation.
- **AI-Support**: Raumbuch-Import aus Text (Gemini 2.0 Flash).
- **Dashboard**: KPI-Übersicht und Entwurfsverwaltung.
- **Sharing**: Teilbare Angebots-Links.
- **Tech**: Python, Streamlit, SQLAlchemy (SQLite/Postgres), Pydantic.

## Installation (Lokal)

1. Repository klonen
2. Environment vorbereiten:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configuration:
   - Erstelle `.env` basierend auf `.env.example`
   - Setze `GEMINI_API_KEY` (optional für AI)
4. Starten:
   ```bash
   streamlit run app.py
   ```
   Login: `admin` / `abc` (oder siehe `auth/auth_config.yaml`)

## Deployment (Production)

1. Datenbank: Postgres (z.B. Neon, Supabase)
2. Config: Setze `DATABASE_URL` in den Environment Variables.
3. Hosting: Streamlit Cloud, Railway, oder Docker.

## Struktur
- `app.py`: Einstiegspunkt & Navigation
- `ui/`: View-Komponenten
- `services/`: Business Logik (Caching aktiv)
- `models/`: Datenbank & Pydantic Schemas
- `data/`: JSON Stammdaten & SQLite DB (Dev)
- `auth/`: Authentifizierung Konfiguration
