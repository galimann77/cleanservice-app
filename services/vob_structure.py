from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class VOBLot:
    id: str
    title: str
    cpv_code: str
    description: str
    turnus: str

@dataclass
class ConstructionServiceItem:
    id: str
    category: str # "floor", "wall", "window", "sanitary", "other"
    name: str # Kurztext
    description: str # Langtext Template
    unit: str # "m2", "Stück", "Psch"
    location_default: str # Default Ort
    is_grob: bool = False
    is_fein: bool = False
    performance: float = 0.0 # m²/h or pcs/h
    wage_type: str = "Sonderreinigung" # "Unterhalt", "Glas", "Sonder"

class VOBStructureService:
    
    @staticmethod
    def get_wage_rates():
        # Hardcoded defaults from Prompt, could also come from DB
        return {
            "Unterhalt": 18.40,
            "Glas": 20.00,
            "Sonder": 19.50
        }

    @staticmethod
    def get_surcharges():
        return {
            "lohnnebenkosten": 0.80, # 80%
            "gemeinkosten": 0.15,    # 15%
            "material": 0.05,        # 5%
            "geraete": 0.02,         # 2%
            "gewinn": 0.25           # 25%
        }

    @staticmethod
    def get_construction_services() -> List[ConstructionServiceItem]:
        return [
            # TITEL 01: BAUGROBREINIGUNG
            ConstructionServiceItem(
                id="01.1", 
                category="grob",
                name="Baugrobreinigung als Zwischenreinigung",
                description="Alle Flächen besenrein abfegen, Grobschmutz und Verpackungsreste entfernen.",
                unit="Psch",
                location_default="EG–2.OG",
                is_grob=True,
                is_fein=False,
                performance=1.0, # Dummy for Pauschal
                wage_type="Sonder"
            ),
            
            # TITEL 02: BAUENDREINIGUNG
            ConstructionServiceItem(
                id="02.1",
                category="floor",
                name="Reinigung Linoleum Boden",
                description="Reinigung des Bodens aus Linoleum. Reinigung der kompletten Bodenbeläge gem. Herstellerangaben, inkl. feucht abwischen der Echtholz-Fußleisten.",
                unit="m²",
                location_default="KG, EG, 1.OG, 2.OG",
                is_grob=False,
                is_fein=True,
                performance=150.0, # m²/h assumption
                wage_type="Unterhalt"
            ),
            ConstructionServiceItem(
                id="02.2",
                category="floor",
                name="Reinigung Vinyl Boden",
                description="Reinigung des Vinyl-Bodenbelags, vollflächig nass reinigen.",
                unit="m²",
                location_default="KG",
                is_grob=False,
                is_fein=True,
                performance=150.0,
                wage_type="Unterhalt"
            ),
            ConstructionServiceItem(
                id="02.3",
                category="floor",
                name="Reinigung Bodenfliesen",
                description="Reinigung der Bodenfliesen, Zementschleier entfernen.",
                unit="m²",
                location_default="EG–3.OG",
                is_grob=False,
                is_fein=True,
                performance=120.0,
                wage_type="Unterhalt"
            ),
            ConstructionServiceItem(
                id="02.4",
                category="wall",
                name="Reinigung Wandfliesen",
                description="Reinigung der Wandfliesen in Sanitärbereichen.",
                unit="m²",
                location_default="WC-Bereiche",
                is_grob=False,
                is_fein=True,
                performance=100.0,
                wage_type="Unterhalt"
            ),
            ConstructionServiceItem(
                id="02.5",
                category="sanitary",
                name="Einrichtungs-/Sanitärgegenstände reinigen",
                description="Sanitärgegenstände (WC, WT, Urinale) komplett reinigen und desinfizieren.",
                unit="Stück",
                location_default="Sanitärräume",
                is_grob=False,
                is_fein=True,
                performance=10.0, # Stk/h
                wage_type="Sonder"
            ),
            ConstructionServiceItem(
                id="02.6",
                category="door",
                name="Innentüren reinigen",
                description="Innentüren inkl. Zargen und Griffe feucht abledern.",
                unit="Stück",
                location_default="KG–2.OG",
                is_grob=False,
                is_fein=True,
                performance=12.0, # Stk/h
                wage_type="Sonder"
            ),
            ConstructionServiceItem(
                id="02.7",
                category="window",
                name="Fenster- u. Brüstungsflügel reinigen",
                description="Glasreinigung 2-seitig inkl. Rahmen und Pfalzen.",
                unit="m²",
                location_default="KG–2.OG",
                is_grob=False,
                is_fein=True,
                performance=25.0, # m²/h
                wage_type="Glas"
            ),
            ConstructionServiceItem(
                id="02.8",
                category="other",
                name="Feinreinigung Möbel",
                description="Feinreinigung Einbaumöbel, Heizkörper, Lichtschalter, Steckdosen.",
                unit="Psch",
                location_default="Alle Bereiche",
                is_grob=False,
                is_fein=True,
                performance=1.0,
                wage_type="Sonder"
            )
        ]

    # ... special items keep existing ...


    @staticmethod
    def get_special_items() -> List[Dict]:
        return [
             {"id": "container_7m3", "name": "Mischcontainer 7m³", "unit": "Stück", "price": 450.00},
             {"id": "bauschutt", "name": "Bauschutt Entsorgung", "unit": "m³", "price": 65.00},
             {"id": "bauaufzug", "name": "Bauaufzug Reinigung", "unit": "Stück", "price": 120.00},
             {"id": "container_buro", "name": "Baucontainer Reinigung", "unit": "Stück", "price": 45.00},
             {"id": "wc_mobil", "name": "Baustellentoilette", "unit": "Stück", "price": 25.00},
             {"id": "vlies_legen", "name": "Abdeckvlies verlegen", "unit": "m²", "price": 3.50},
             {"id": "vlies_weg", "name": "Abdeckvlies entsorgen", "unit": "m²", "price": 1.80}
        ]
