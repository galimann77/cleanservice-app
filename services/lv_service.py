from dataclasses import dataclass, field, asdict
from typing import List, Optional
import pandas as pd
from datetime import datetime

@dataclass
class LVPosition:
    """Represents a single item in the Bill of Quantities (Leistungsverzeichnis)."""
    oz: str         # Ordnungszahl (e.g., 01.01.001)
    titel: str      # Title/Los (e.g., Baureinigung)
    kurztext: str   # Short description
    langtext: str   # Full detailed description (STLB style)
    menge: float    # Quantity
    einheit: str    # Unit (m2, Stk, h)
    ep: float       # Unit Price
    gp: float       # Total Price (Menge * EP)
    
    # Meta attributes for GAEB mapping later
    stlb_lb: str = "033" # Standardleistungsbereich (033 = Gebäudereinigung)
    art: str = "Normal" # Normal, Bedarfs, etc.

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return LVPosition(**data)

@dataclass
class LVProject:
    """Container for the entire LV."""
    name: str # Project Name
    date: str
    positions: List[LVPosition] = field(default_factory=list)
    
    def get_total_net(self):
        return sum(p.gp for p in self.positions)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        positions_data = data.get('positions', [])
        positions = [LVPosition.from_dict(p) for p in positions_data]
        return LVProject(
            name=data.get('name', 'Unbenannt'),
            date=data.get('date', ''),
            positions=positions
        )

class LVGenerator:
    """Service to generate LV text and structure from calculation data."""
    
    @staticmethod
    def generate_langtext(service_type, attributes):
        """
        Generates a STLB-like long text based on attributes.
        attributes dict:
        - nutzung: Büro, Schule, etc.
        - boden: PVC, Stein, etc.
        - verschmutzung: grob, fein, stark
        - leistung: reinigen, beschichten, etc.
        """
        
        # Base Text Blocks
        header = f"Ausführen von {service_type} in {attributes.get('nutzung', 'Gebäuden')}."
        
        body = []
        
        # 1. Surface / Substrate
        if "boden" in attributes:
            body.append(f"Untergrund: {attributes['boden']}.")
        
        # 2. Scope / Performance
        if "grob" in service_type.lower():
            body.append("Leistungsumfang: Beseitigen von Grobschmutz, Bauschutt, Verpackungsresten und mörtelartigen Anhaftungen. Besenreine Übergabe.")
        elif "fein" in service_type.lower():
            body.append("Leistungsumfang: Beseitigen von Reststaub und haftenden Verschmutzungen auf allen Oberflächen (boden, wand, decke, inventar).")
            body.append("Inklusive Nassreinigung der Bodenbeläge mit geeignetem Reinigungsmittel.")
            body.append("Inklusive Einpflege/Erstpflege gemäß Herstellervorgaben.")
        
        # 3. Constraints/Details
        if attributes.get("verschmutzung") == "stark":
             body.append("Erschwernis: Starker Verschmutzungsgrad durch vorangegangene Ausbauarbeiten.")
        
        body.append("Abrechnung nach tatsächlichem Aufmaß.")
        
        return f"{header}\n\n{' '.join(body)}"

    @staticmethod
    def create_position_from_calc(calc_item, index, attributes=None):
        """
        Transforms a calculation item into an LVPosition.
        """
        attributes = attributes or {}
        
        # Formatting OZ: 01.01.001
        # Assuming Title is fixed to 01 for now or passed in attributes
        titel_idx = attributes.get("titel_idx", 1)
        oz = f"{titel_idx:02d}.{index:02d}.0010"
        
        kurztext = calc_item.get("pos")
        # Enhance Kurztext
        if attributes.get("boden"):
            kurztext += f" ({attributes['boden']})"
            
        full_text = LVGenerator.generate_langtext(calc_item.get("art", "Reinigung"), attributes)
        
        return LVPosition(
            oz=oz,
            titel=attributes.get("titel_name", "Allgemein"),
            kurztext=kurztext,
            langtext=full_text,
            menge=calc_item.get("menge", 0),
            einheit=calc_item.get("unit", "Stk"),
            ep=calc_item.get("ep", 0.0),
            gp=calc_item.get("gp", 0.0)
        )
