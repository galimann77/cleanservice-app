# CLEANSERVICE 5.0 - Changelog

## Phase 1: Architektur
- ✅ **Caching**: `st.cache_resource` und `st.cache_data` für AI & Berechnungen implementiert.
- ✅ **Database**: Postgres-ready Config und Connection Pooling.
- ✅ **Drafts**: Auto-Save System für Projektdaten.

## Phase 2: Features
- ✅ **Express-Modus**: Schnelle Preisindikation in 30 Sekunden mit ±15% Toleranz.
- ✅ **Rüstzeiten**: Berechnung berücksichtigt Rüstzeiten (Data-Driven).
- ✅ **Plausibilitätsprüfung**: Automatische Warnung bei Abweichungen.
- ✅ **Foto-Upload**: Vorbereitung für AI-Vision (Speicherung als JSON).

## Phase 3: UX
- ✅ **Dashboard**: Neue Startseite mit KPIs und "Zuletzt bearbeitet".
- ✅ **Navigation**: Verbesserte Struktur (Sidebar).
- ✅ **Angebot-Sharing**: Generierung externer Links für Kunden.

## Phase 4: Security
- ✅ **Auth**: Neues `auth/` Modul mit `streamlit-authenticator` v0.3.3 Integration.
- ✅ **Config**: Zentrale `config.py` mit Environment-Support.

## Gelöschte Features
- ❌ "Treppenhausreinigung" (redundant, integriert in Unterhalt).
- ❌ "Industriereinigung" (obsolet).
