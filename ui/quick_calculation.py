import streamlit as st
import pandas as pd
from services.market_analytics import MarketAnalyticsService
from services.gemini_client import GeminiClient

def render_quick_calculation():
    st.title("⚡ Schnellkalkulation")
    st.caption("Ermitteln Sie blitzschnell eine Preisschätzung mit automatischer KI-Plausibilitätsprüfung.")

    analytics = MarketAnalyticsService()

    # --- INPUTS ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Objektdaten")
        # Erweiterte Liste
        service_types = [
            "Büroreinigung (Unterhalt)", 
            "Glasreinigung (mit Rahmen)", 
            "Grundreinigung (Boden)", 
            "Baureinigung (Grob)", 
            "Baureinigung (Fein)", 
            "Teppichreinigung (Sprühextraktion)", 
            "Treppenhausreinigung",
            "Fassadenreinigung",
            "Industriereinigung"
        ]
        service_type = st.selectbox("Reinigungsart", service_types)
        
        unit = "m²"
        if "Treppenhaus" in service_type: unit = "Etagen"
        
        amount = st.number_input(f"Menge ({unit})", min_value=1.0, value=100.0, step=10.0)

    with col2:
        st.subheader("2. Spezifische Faktoren")
        
        # Dynamische Faktoren basierend auf Typ (Vereinfacht für Demo, aber erweiterbar)
        # Region removed as per user request (Standard assumed)
        region = "Standard" 
        
        if "Büro" in service_type or "Unterhalt" in service_type:
            dirt = st.selectbox("Nutzungsintensität", ["Normal (Büro)", "Hoch (Praxis/Kita)", "Extrem (Werkstatt)"])
        elif "Bau" in service_type:
             dirt = st.selectbox("Verschmutzung", ["Besenrein", "Mörtelreste/Farbe", "Extrem"])
        else:
             dirt = st.selectbox("Schwierigkeitsgrad", ["Normal", "Schwer (Zugang/Höhe)", "Extrem"])
             
        freq = st.selectbox("Turnus", ["Einmalig", "Wöchentlich", "Monatlich"])

    # --- ACTION ---
    
    if st.button("💰 Preis berechnen & Prüfen", type="primary"):
        # 1. Marktpreis Recherche (Live-Simulation)
        with st.spinner("Recherchiere aktuelle Marktpreise..."):
            market_data = analytics.research_market_prices(service_type, region)
        
        # Basis-Preis (vom recherchierten Mittelwert)
        base_price_sqm = market_data["avg_price"]
        
        # Faktoren anwenden
        factor = 1.0
        if "Hoch" in dirt or "Schwer" in dirt or "Mörtel" in dirt: factor += 0.25
        if "Extrem" in dirt: factor += 0.50
        
        final_price_sqm = base_price_sqm * factor
        
        # Range +/- 15% (Express Calculation Requirement)
        price_min = final_price_sqm * 0.85
        price_max = final_price_sqm * 1.15
        
        total_price = final_price_sqm * amount
        total_min = total_price * 0.85
        total_max = total_price * 1.15
        
        # Plausibilitäts-Check
        check_result = analytics.check_plausibility(service_type, amount, final_price_sqm, total_price)
        
        # --- ERGEBNIS ANZEIGE ---
        
        st.markdown("---")
        st.subheader("📊 Ergebnis: Kalkulation")
        
        m1, m2, m3 = st.columns(3)
        st.info("ℹ️ **Express-Kalkulation**: Schnelle Richtpreisindikation mit ±15% Toleranz")

        m1.metric("Marktpreis (Ø)", f"{base_price_sqm:.2f} €/{unit}")
        m2.metric("Ihr Kalkulationspreis", f"{final_price_sqm:.2f} €/{unit}", delta=f"Faktor {factor}x")
        
        m3.metric(
            "Richtpreis (Netto)", 
            f"{total_price:,.2f} €",
            delta=f"±15% = {total_min:,.2f} - {total_max:,.2f} €",
            delta_color="off"
        )
        
        st.markdown(f"**Brutto (inkl. 19%):** {(total_price*1.19):.2f} €")
        
        # Recherche Details
        with st.expander("🔍 Details der Marktpreis-Recherche", expanded=False):
            st.write(f"Durchschnitt aus {len(market_data['sources'])} Quellen:")
            for s in market_data['sources']:
                st.caption(f"- {s['quelle']}: {s['preis']:.2f} € ({s['datum']})")
                
        # Plausibilität
        if check_result["status"] == "warnung":
            st.warning("⚠️ **Automatische Plausibilitätsprüfung**")
            for w in check_result["warnungen"]:
                st.write(f"- {w}")
            
            st.markdown("##### 💡 Optimierungsvorschläge")
            for e in check_result["empfehlungen"]:
                st.info(e)
        else:
            st.success("✅ Kalkulation liegt im plausiblen Marktbereich.")
            
        # KI Analyse (Optional)
        st.markdown("---")
        if st.checkbox("🤖 Detaillierte KI-Analyse anfordern (Gemini)"):
            with st.spinner("Gemini analysiert Ihre Kalkulation..."):
                client = GeminiClient()
                if not client.client: # Check if client initialized
                     st.error("Kein API Key gefunden.")
                else:
                    summary = f"""
                    Kalkulation: {service_type}
                    Menge: {amount} {unit}
                    Region: {region}
                    Erschwernis: {dirt}
                    
                    Ermittelter Preis: {final_price_sqm:.2f} EUR/{unit}
                    Gesamtpreis: {total_price:.2f} EUR
                    
                    Markt-Vergleich (Min/Max): {check_result['limits']['min']} - {check_result['limits']['max']}
                    """
                    analysis = client.check_plausibility(summary)
                    st.markdown(analysis)

