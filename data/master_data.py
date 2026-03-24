# Master Data Structure (Stammdaten) based on Analysis
# Source: CleanManager / Profacilo Analysis via User Prompt

stammdaten_struktur = {
    "unternehmen": {
        "firmenname": "",
        "standort": "Herten, NRW",
        "strasse_hausnr": "",
        "plz_ort": "",
        "telefon": "",
        "email": "",
        "steuernummer": "",
        "ust_id": "",
    },
    "lohnkosten": {
        "stundenlohn_unterhaltsreinigung": 18.40,  # Tariflohn 2026 Estimate
        "stundenlohn_glasreinigung": 20.00,
        "stundenlohn_grundreinigung": 19.00,
        "stundenlohn_sonderreinigung": 19.50,
        "lohnzuschlag_prozent": 25.0,  # Sozialabgaben, Urlaub, Weiterbildung
        "personalkosten_pro_stunde_auto": 0.0  # Automatisch berechnet
    },
    "material_overhead": {
        "materialprozentsatz": 5.0,  # 3-7% üblich für Standard-Reinigungsmittel
        "overhead_verwaltung_prozent": 15.0,  # Büro, Verwaltung, Versicherungen
        "ziel_gewinnmarge_prozent": 25.0  # Zielmarge für Angebotspreis
    },
    "zuschlaege": {
        "abendzuschlag_prozent": 15.0,  # z.B. 18:00-22:00 Uhr
        "nachtzuschlag_prozent": 25.0,  # z.B. 22:00-06:00 Uhr
        "sonntagszuschlag_prozent": 50.0,
        "feiertagszuschlag_prozent": 125.0,
        "regionalfaktor_nrw_prozent": 10.0  # +10% für NRW (teurer als Ostdeutschland)
    },
    "sonstiges": {
        "anfahrt_preis_pro_km": 0.70,
        "anfahrtspauschale_unter_x_stunden": 25.00,
        "mindeststunden_pro_auftrag": 2.0,
        "waehrung": "EUR",
        "mwst_prozent": 19.0
    },
    "benutzerdefiniert": {
        "feld_1": {"label": "Grundreinigung Pauschale", "wert": 0.0},
        "feld_2": {"label": "Maschinenvermietung pro Tag", "wert": 0.0},
        "feld_3": {"label": "Sonderleistung XY", "wert": 0.0},
    }
}
