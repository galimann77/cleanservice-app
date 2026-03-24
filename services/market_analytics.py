import streamlit as st
import random
from datetime import datetime

class MarketAnalyticsService:
    @staticmethod
    def get_price_limits():
        return {
            "Büroreinigung (Unterhalt)": {"min": 0.80, "max": 2.50},
            "Grundreinigung (Boden)": {"min": 3.00, "max": 8.00},
            "Glasreinigung (mit Rahmen)": {"min": 2.50, "max": 6.00},
            "Baureinigung (Grob)": {"min": 5.00, "max": 15.00},
            "Baureinigung (Fein)": {"min": 6.00, "max": 18.00},
            "Fassadenreinigung": {"min": 8.00, "max": 25.00},
            "Industriereinigung": {"min": 1.50, "max": 5.00},
            "Teppichreinigung (Sprühextraktion)": {"min": 2.50, "max": 6.50},
            "Treppenhausreinigung": {"min": 8.00, "max": 20.00}
        }

    @staticmethod
    def check_plausibility(service_type: str, area: float, price_per_unit: float, total_price: float):
        """
        Prüft Kalkulation auf Plausibilität.
        """
        warnungen = []
        empfehlungen = []
        status = "ok"
        
        limits = MarketAnalyticsService.get_price_limits().get(service_type, {"min": 0.50, "max": 30.00})
        
        # 1. Preis Check
        if price_per_unit < limits["min"]:
            warnungen.append(f"⚠️ Preis ({price_per_unit:.2f} €) liegt UNTER Marktstandard ({limits['min']:.2f} €)")
            empfehlungen.append(f"💡 Empfehlung: Erhöhe auf mind. {limits['min']:.2f} € (Gesamt: {area * limits['min']:.2f} €)")
            status = "warnung"
        elif price_per_unit > limits["max"]:
            warnungen.append(f"⚠️ Preis ({price_per_unit:.2f} €) liegt ÜBER Marktstandard ({limits['max']:.2f} €)")
            empfehlungen.append(f"💡 Risiko: Angebot könnte abgelehnt werden. Prüfe Leistungen.")
            status = "warnung" # Optional, maybe just info
            
        # 2. Flächen Check
        if area < 10 and area > 0:
             warnungen.append("⚠️ Sehr kleine Fläche - Mindestpauschale empfohlen")
             empfehlungen.append(f"💡 Empfehlung: Setze Mindestpauschale (z.B. 80-120 €) statt {total_price:.2f} €")
             status = "warnung"

        # 3. Wirtschaftlichkeit
        if total_price < 50:
            warnungen.append("⚠️ Auftragswert unter Wirtschaftlichkeitsgrenze")
            empfehlungen.append("💡 Empfehlung: Anfahrtspauschale berechnen oder ablehnen.")
            status = "warnung"
            
        return {"warnungen": warnungen, "empfehlungen": empfehlungen, "status": status, "limits": limits}

    @staticmethod
    def research_market_prices(service_type: str, region: str = "NRW"):
        """
        Simuliert eine Marktpreisrecherche auf Fachportalen.
        In Produktion würde hier echtes Scraping oder API-Call stattfinden.
        """
        # Mock Data Generation based on real ranges with slight randomization 
        # to simulate "live" findings
        limits = MarketAnalyticsService.get_price_limits().get(service_type, {"min": 2.00, "max": 10.00})
        
        base_min = limits["min"]
        base_max = limits["max"]
        
        # Region factor
        factor = 1.0
        if "München" in region: factor = 1.2
        if "Ost" in region: factor = 0.9
        
        # Simulate found articles
        current_month = datetime.now().strftime("%Y-%m")
        
        # Generate 3 "sources"
        found_prices = [
            {"quelle": "rationell-reinigen.de", "preis": base_min * factor * 1.05 + random.uniform(0, 0.5), "datum": current_month},
            {"quelle": "die-gebaeudedienstleister.de", "preis": (base_min + base_max)/2 * factor, "datum": "2025-12"},
            {"quelle": "clean-magazin.de", "preis": base_max * factor * 0.90 - random.uniform(0, 0.5), "datum": "2025-11"}
        ]
        
        avg_price = sum(p["preis"] for p in found_prices) / len(found_prices)
        
        return {
            "avg_price": avg_price,
            "sources": found_prices
        }
