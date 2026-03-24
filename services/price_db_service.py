from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class PricePosition:
    id: str
    pos_nr: str
    kurztext: str
    langtext: str
    ort: str
    leistung_m2_h: float
    einheit: str
    ep_basis: float
    turnus_faktoren: Dict[str, float]
    material_anteil: float
    stundensatz_ref: str
    nebenleistungen: List[str]

@dataclass
class CleaningCategory:
    id: str
    name: str # e.g. "Unterhaltsreinigung"
    lb_code: str # "033"
    description: str
    positions: List[PricePosition]

class PriceDatabaseService:
    """
    Central Repository for Standard Market Prices and Service Descriptions.
    Based on real data from NRW/Herten context.
    """
    
    @staticmethod
    def get_database() -> List[CleaningCategory]:
        return [
            # 1. UNTERHALTSREINIGUNG
            CleaningCategory(
                id="unterhaltsreinigung",
                name="Unterhaltsreinigung",
                lb_code="033",
                description="Laufende Unterhaltsreinigung von Gebäuden",
                positions=[
                    PricePosition(
                        id="UR-001",
                        pos_nr="001",
                        kurztext="Büroreinigung Standard",
                        langtext="Reinigung von Büroräumen inkl. Schreibtische abwischen, Papierkörbe leeren, Bodenbelag kehren/wischen, Türgriffe reinigen, Lichtschalter säubern. Ausführung gem. RAL-GZ 902.",
                        ort="Büroräume allgemein",
                        leistung_m2_h=200.0,
                        einheit="m²",
                        ep_basis=0.85,
                        turnus_faktoren={
                            "taeglich": 1.0, "3x_woche": 1.15, "2x_woche": 1.30, "1x_woche": 1.50, "14_taegig": 1.80
                        },
                        material_anteil=5.0,
                        stundensatz_ref="wage_maintenance",
                        nebenleistungen=["Papierkörbe leeren", "Schreibtische entstauben", "Türgriffe desinfizieren"]
                    ),
                    PricePosition(
                        id="UR-002",
                        pos_nr="002",
                        kurztext="Sanitärreinigung Standard",
                        langtext="Reinigung von Sanitärräumen inkl. WC-Becken reinigen/desinfizieren, Waschbecken entkalken, Spiegel streifenfrei, Armaturen polieren, Spender auffüllen, Böden nasswischen, Fliesen reinigen.",
                        ort="Sanitärräume, WC-Anlagen",
                        leistung_m2_h=25.0,
                        einheit="m²",
                        ep_basis=3.20,
                        turnus_faktoren={
                            "taeglich": 1.0, "3x_woche": 1.10, "2x_woche": 1.25, "1x_woche": 1.45
                        },
                        material_anteil=8.0,
                        stundensatz_ref="wage_special",
                        nebenleistungen=["WC-Becken desinfizieren", "Spender auffüllen", "Abflüsse säubern"]
                    ),
                    PricePosition(
                        id="UR-003",
                        pos_nr="003",
                        kurztext="Treppenhaus/Flure reinigen",
                        langtext="Reinigung von Treppenhäusern und Fluren inkl. Böden kehren/wischen, Treppenstufen reinigen, Handläufe abwischen, Türen/Zargen säubern, Briefkästen reinigen.",
                        ort="Treppenhäuser, Verkehrsflächen",
                        leistung_m2_h=300.0,
                        einheit="m²",
                        ep_basis=0.60,
                        turnus_faktoren={
                            "1x_woche": 1.0, "14_taegig": 1.20, "monatlich": 1.50
                        },
                        material_anteil=3.0,
                        stundensatz_ref="wage_maintenance",
                        nebenleistungen=["Handläufe desinfizieren", "Briefkästen entstauben"]
                    ),
                    PricePosition(
                        id="UR-004",
                        pos_nr="004",
                        kurztext="Küchenreinigung Teeküche",
                        langtext="Reinigung von Teeküchen/Pantries inkl. Arbeitsflächen desinfizieren, Spüle/Armatur reinigen, Herd/Mikrowelle außen, Kühlschrank außen, Schränke außen, Böden nasswischen, Müll entsorgen.",
                        ort="Teeküchen, Pantries",
                        leistung_m2_h=40.0,
                        einheit="m²",
                        ep_basis=2.80,
                        turnus_faktoren={
                            "taeglich": 1.0, "3x_woche": 1.12, "2x_woche": 1.30
                        },
                        material_anteil=7.0,
                        stundensatz_ref="wage_special",
                        nebenleistungen=["Müll entsorgen", "Spülmaschine außen reinigen"]
                    )
                ]
            ),
            
            # 2. GLASREINIGUNG
            CleaningCategory(
                id="glasreinigung",
                name="Glas- und Rahmenreinigung",
                lb_code="033",
                description="Glas- und Rahmenreinigung",
                positions=[
                    PricePosition(
                        id="GR-001",
                        pos_nr="001",
                        kurztext="Fensterreinigung innen/außen mit Rahmen",
                        langtext="Reinigung von Fenstern beidseitig (innen/außen) inkl. Rahmen komplett, Fensterbänke innen/außen, Dichtungsgummis. Streifen- und fleckenfrei. Ausführung gem. RAL-GZ 902.",
                        ort="Alle Fenster",
                        leistung_m2_h=80.0,
                        einheit="m²",
                        ep_basis=9.50,
                        turnus_faktoren={
                            "1x_jahr": 1.15, "2x_jahr": 1.0, "4x_jahr": 0.90, "6x_jahr": 0.82, "monatlich": 0.75
                        },
                        material_anteil=3.0,
                        stundensatz_ref="wage_glass",
                        nebenleistungen=["Rahmen komplett reinigen", "Fensterbänke innen/außen", "Gummi säubern"]
                    ),
                    PricePosition(
                        id="GR-002",
                        pos_nr="002",
                        kurztext="Glasreinigung nur innen",
                        langtext="Reinigung von Fenstern einseitig (nur innen) inkl. Rahmen innen, Fensterbänke innen. Streifen- und fleckenfrei.",
                        ort="Alle Fenster",
                        leistung_m2_h=120.0,
                        einheit="m²",
                        ep_basis=5.80,
                        turnus_faktoren={
                            "1x_jahr": 1.20, "2x_jahr": 1.0, "4x_jahr": 0.88, "monatlich": 0.72
                        },
                        material_anteil=2.0,
                        stundensatz_ref="wage_glass",
                        nebenleistungen=["Rahmen innen reinigen", "Fensterbänke innen"]
                    ),
                     PricePosition(
                        id="GR-003",
                        pos_nr="003",
                        kurztext="Glasfassadenreinigung",
                        langtext="Reinigung von Glasfassaden inkl. Großflächenfenster, Rahmenelemente, Silikonfugen, Aluminiumprofile. Hubsteiger/Gerüst erforderlich. Ausführung nach Herstellervorgaben.",
                        ort="Fassade",
                        leistung_m2_h=40.0,
                        einheit="m²",
                        ep_basis=15.00,
                        turnus_faktoren={
                            "1x_jahr": 1.0, "2x_jahr": 0.85
                        },
                        material_anteil=5.0,
                        stundensatz_ref="wage_glass",
                        nebenleistungen=["Hubsteiger (sep.)", "Silikonfugen", "Aluprofile"]
                    )
                ]
            ),
            
            # 3. GRUNDREINIGUNG (Sample, incomplete in prompt but I will add standard item)
             CleaningCategory(
                id="grundreinigung",
                name="Grund- und Sonderreinigung",
                lb_code="033",
                description="Intensivreinigung von Bodenbelägen und Oberflächen",
                positions=[
                     PricePosition(
                        id="SDR-001",
                        pos_nr="001",
                        kurztext="Grundreinigung PVC/Linoleum beschichtet",
                        langtext="Maschinelle Grundreinigung von elastischen Bodenbelägen. Entfernung alter Beschichtungen. Neutralisieren und 2-fache Neubeschichtung mit Polymerdispersion.",
                        ort="Bodenflächen",
                        leistung_m2_h=15.0,
                        einheit="m²",
                        ep_basis=6.50,
                        turnus_faktoren={"einmalig": 1.0},
                        material_anteil=12.0,
                        stundensatz_ref="wage_special",
                        nebenleistungen=["Alte Beschichtung entfernen", "Neubeschichtung"]
                    )
                ]
             )
        ]
