from core.database import get_db
from models.offer import Offer
import uuid
import json

class OfferService:
    
    @staticmethod
    def create_shareable_offer(project_data: dict, user_id: str) -> str:
        """
        Erstellt teilbares Angebot und gibt Share-URL zurück.
        """
        # Get a new session
        db = next(get_db())
        try:
            offer_id = str(uuid.uuid4())
            
            # Extract basic info from dict
            cost_summary = project_data.get("cost_summary", {})
            total_net = cost_summary.get("total_net_monthly", 0.0)
            customer = project_data.get("project_name", "Unbenannt") # Mapping might vary
            
            offer = Offer(
                offer_id=offer_id,
                user_id=user_id,
                customer_name=customer,
                total_price=total_net,
                data_json=json.dumps(project_data, default=str),
                is_public=1
            )
            
            db.add(offer)
            db.commit()
            
            # URL generieren (später über env-config)
            # For now use localhost or Streamlit Cloud logic
            base_url = "https://cleanservice-app.streamlit.app" 
            share_url = f"{base_url}/?offer_id={offer_id}"
            
            return share_url
        finally:
            db.close()
    
    @staticmethod
    def get_offer_by_id(offer_id: str):
        """Lädt Angebot für Read-Only-Ansicht."""
        db = next(get_db())
        try:
            offer = db.query(Offer).filter_by(
                offer_id=offer_id,
                is_public=1
            ).first()
            return offer
        finally:
            db.close()
