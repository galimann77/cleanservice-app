# Professional Cleaning Service Catalog (Reinigungsarten)
# Includes Industry Standard Performance Values (m²/h) and Pricing Benchmarks

reinigungsarten_vollstaendig = {
    "unterhaltsreinigung": {
        "label": "Unterhaltsreinigung",
        "icon": "🧹",
        "beschreibung": "Regelmäßige Reinigung von Büros, Nutzflächen und Sanitär.",
        "typen": {
            "buero_standard": {
                "label": "Büro (Standard)",
                "leistungswert_m2_h": 200,
                "leistungswert_min": 170,
                "leistungswert_max": 230,
                "basis_preis_m2_min": 2.20,
                "basis_preis_m2_max": 3.80,
                "beschreibung": "Schreibtische (frei), Böden saugen/wischen, Papierkörbe, Griffspuren.",
                "raumgruppe": "Büro"
            },
            "buero_voll": {
                "label": "Büro (Überstellt/Detailliert)",
                "leistungswert_m2_h": 150,
                "leistungswert_min": 120,
                "leistungswert_max": 180,
                "basis_preis_m2_min": 2.80,
                "basis_preis_m2_max": 4.50,
                "beschreibung": "Viel Mobiliar, Fensterbänke, detaillierte Staubwischen, Monitore.",
                "raumgruppe": "Büro"
            },
            "sanitaer_standard": {
                "label": "Sanitäranlagen (Unterhalt)",
                "leistungswert_m2_h": 60,
                "leistungswert_min": 45,
                "leistungswert_max": 80,
                "basis_preis_m2_min": 4.50,
                "basis_preis_m2_max": 7.00,
                "beschreibung": "WC-Becken, Urinale, Waschbecken, Spiegel, Böden nass, Auffüllen.",
                "raumgruppe": "Sanitär"
            },
            "flur_treppe": {
                "label": "Verkehrsflächen (Flur/Treppe)",
                "leistungswert_m2_h": 300,
                "leistungswert_min": 250,
                "leistungswert_max": 350,
                "basis_preis_m2_min": 1.50,
                "basis_preis_m2_max": 2.50,
                "beschreibung": "Böden wischen/saugen, Handläufe, wenig Inventar.",
                "raumgruppe": "Flur"
            },
            "lager_halle": {
                "label": "Lagerhalle / Industrie (Leer)",
                "leistungswert_m2_h": 600,
                "leistungswert_min": 450,
                "leistungswert_max": 800,
                "basis_preis_m2_min": 0.50,
                "basis_preis_m2_max": 1.50,
                "beschreibung": "Maschinelle Bodenreinigung, große freie Flächen.",
                "raumgruppe": "Gewerbe"
            },
            "kita_schule": {
                "label": "Kita / Schule (Gruppenraum)",
                "leistungswert_m2_h": 120,
                "leistungswert_min": 100,
                "leistungswert_max": 150,
                "basis_preis_m2_min": 3.00,
                "basis_preis_m2_max": 5.00,
                "beschreibung": "Tische, Stühle aufstuhlen, Waschbecken, Böden, Spielbereiche.",
                "raumgruppe": "Sozial"
            }
        }
    },
    "glasreinigung": {
        "label": "Glas- & Fassadenreinigung",
        "icon": "🪟",
        "beschreibung": "Professionelle Fensterreinigung inkl. Rahmen und Falzen.",
        "typen": {
            "schaufenster": {
                "label": "Schaufenster (Großfläche)",
                "leistungswert_m2_h": 100,
                "leistungswert_min": 80,
                "leistungswert_max": 120,
                "basis_preis_m2_min": 1.50,
                "basis_preis_m2_max": 3.00,
                "beschreibung": "Große durchgehende Flächen, einfach erreichbar (ohne Leiter).",
                "schwierigkeit": "Einfach"
            },
            "fenster_bestand": {
                "label": "Fenster (Dreh-Kipp, 2-seitig)",
                "leistungswert_m2_h": 20,
                "leistungswert_min": 15,
                "leistungswert_max": 25,
                "basis_preis_m2_min": 4.50,
                "basis_preis_m2_max": 7.50,
                "beschreibung": "Inkl. Rahmenwäsche und Falzreinigung. Standard Bürofenster.",
                "schwierigkeit": "Mittel"
            },
            "fenster_kasten": {
                "label": "Kastenfenster (Altbau, 4-seitig)",
                "leistungswert_m2_h": 8,
                "leistungswert_min": 5,
                "leistungswert_max": 12,
                "basis_preis_m2_min": 9.00,
                "basis_preis_m2_max": 16.00,
                "beschreibung": "Verbundfenster zum Aufschrauben, 4 Glasseiten, aufwendige Rahmen.",
                "schwierigkeit": "Sehr Hoch"
            },
            "sprossenfenster": {
                "label": "Sprossenfenster",
                "leistungswert_m2_h": 6,
                "leistungswert_min": 4,
                "leistungswert_max": 9,
                "basis_preis_m2_min": 10.00,
                "basis_preis_m2_max": 20.00,
                "beschreibung": "Kleinteilige Glasflächen, hoher Zeitaufwand für Ecken.",
                "schwierigkeit": "Extrem Hoch"
            },
            "glasdach_wintergarten": {
                "label": "Glasdach / Wintergarten",
                "leistungswert_m2_h": 15,
                "leistungswert_min": 10,
                "leistungswert_max": 20,
                "basis_preis_m2_min": 6.00,
                "basis_preis_m2_max": 12.00,
                "beschreibung": "Überkopfverglasung, oft Leitereinsatz nötig.",
                "schwierigkeit": "Hoch"
            },
            "fassade_eloxal": {
                "label": "Fassadenreinigung (Eloxal/Metall)",
                "leistungswert_m2_h": 30,
                "leistungswert_min": 20,
                "leistungswert_max": 40,
                "basis_preis_m2_min": 8.00,
                "basis_preis_m2_max": 15.00,
                "beschreibung": "Reinigung und Konservierung von Metallfassaden.",
                "schwierigkeit": "Hoch"
            }
        }
    },
    "sonderreinigung": {
        "label": "Grund- & Sonderreinigung",
        "icon": "✨",
        "beschreibung": "Intensivreinigungen, Baureinigung und Spezialaufträge.",
        "typen": {
            "grundreinigung_pvc": {
                "label": "Grundreinigung PVC/Linoleum (+Beschichtung)",
                "leistungswert_m2_h": 15,
                "leistungswert_min": 10,
                "leistungswert_max": 20,
                "basis_preis_m2_min": 9.00,
                "basis_preis_m2_max": 14.00,
                "beschreibung": "Maschinelles Entschichten, Neutralisieren, 2-3 Schichten Polymer.",
                "materialaufwand": "Hoch"
            },
            "teppich_sprueh": {
                "label": "Teppichreinigung (Sprühextraktion)",
                "leistungswert_m2_h": 40,
                "leistungswert_min": 30,
                "leistungswert_max": 60,
                "basis_preis_m2_min": 4.50,
                "basis_preis_m2_max": 8.00,
                "beschreibung": "Nassreinigung mit Extraktionsgerät für Tiefenschmutz.",
                "materialaufwand": "Mittel"
            },
            "teppich_shampoonierung": {
                "label": "Teppichreinigung (Shampoonierung)",
                "leistungswert_m2_h": 25,
                "leistungswert_min": 20,
                "leistungswert_max": 35,
                "basis_preis_m2_min": 6.00,
                "basis_preis_m2_max": 10.00,
                "beschreibung": "Einscheibenmaschine mit Bürste und Schaum.",
                "materialaufwand": "Mittel"
            },
            "bauendreinigung_fein": {
                "label": "Bauendreinigung (Bezugsfertig)",
                "leistungswert_m2_h": 35,
                "leistungswert_min": 25,
                "leistungswert_max": 50,
                "basis_preis_m2_min": 5.00,
                "basis_preis_m2_max": 9.00,
                "beschreibung": "Entfernung von Handwerkerschmutz, Folien, Etiketten, Staubfrei.",
                "materialaufwand": "Mittel"
            },
            "bau_grob": {
                "label": "Baugrobreinigung (Besenrein)",
                "leistungswert_m2_h": 80,
                "leistungswert_min": 60,
                "leistungswert_max": 120,
                "basis_preis_m2_min": 2.50,
                "basis_preis_m2_max": 4.50,
                "beschreibung": "Entfernung von Bauschuttresten, Verpackungsmaterial, Grobschmutz.",
                "materialaufwand": "Gering"
            }
        }
    },
    "steinreinigung": {
        "label": "Stein- & Außenreinigung",
        "icon": "🧱",
        "beschreibung": "Hochdruck- und Spezialreinigung von Außenflächen.",
        "typen": {
            "pflaster_hd": {
                "label": "Pflasterreinigung (Hochdruck)",
                "leistungswert_m2_h": 70,
                "leistungswert_min": 50,
                "leistungswert_max": 100,
                "basis_preis_m2_min": 5.00,
                "basis_preis_m2_max": 9.00,
                "beschreibung": "Entfernung von Moos, Algen, Flechten mittels Hochdruck.",
                "zubehoer": ["Fugen reinigen", "Nachsanden"]
            },
            "terrasse_stein": {
                "label": "Terrassenreinigung (Naturstein)",
                "leistungswert_m2_h": 40,
                "leistungswert_min": 25,
                "leistungswert_max": 60,
                "basis_preis_m2_min": 8.00,
                "basis_preis_m2_max": 15.00,
                "beschreibung": "Schonende Reinigung, ggf. chemische Vorbehandlung.",
                "zubehoer": ["Imprägnieren"]
            }
        }
    }
}
