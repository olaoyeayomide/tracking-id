# Create a script to seed initial carriers
# backend/scripts/seed_carriers.py
"""
Script to seed initial carriers into the database
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connection import SessionLocal
from app.models.carrier import Carrier, CarrierType, CarrierStatus
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_carriers():
    """Seed initial carriers into the database"""
    db = SessionLocal()

    try:
        # Check if carriers already exist
        existing_count = db.query(Carrier).count()
        if existing_count > 0:
            logger.info(
                f"Database already has {existing_count} carriers. Skipping seeding."
            )
            return

        carriers = [
            # API-Based Carriers
            {
                "name": "Sendbox",
                "code": "sendbox",
                "description": "Sendbox Logistics - Nigerian delivery service",
                "type": CarrierType.API,
                "status": CarrierStatus.ACTIVE,
                "api_endpoint": "https://api.sendbox.co/v1/shipments/{tracking_id}/track",
                "auth_type": "api_key",
                "auth_config": {"header_name": "Authorization", "prefix": "Bearer"},
                "webhook_verification": True,
                "webhook_url": "https://your-domain.com/webhooks/sendbox",
                "tracking_url_template": "https://sendbox.co/tracking/{tracking_id}",
                "tracking_id_pattern": "^SBX\\d{10}$",
                "country": "Nigeria",
                "support_phone": "+2347000000000",
                "support_email": "support@sendbox.co",
            },
            {
                "name": "DHL Express Nigeria",
                "code": "dhl",
                "description": "DHL International Express shipping",
                "type": CarrierType.API,
                "status": CarrierStatus.ACTIVE,
                "api_endpoint": "https://api.dhl.com/track/shipments",
                "auth_type": "api_key",
                "auth_config": {"header_name": "DHL-API-Key", "prefix": ""},
                "tracking_url_template": "https://www.dhl.com/ng-en/home/tracking/tracking-express.html?submit=1&tracking-id={tracking_id}",
                "tracking_id_pattern": "^\\d{10,11}$",
                "country": "International",
                "support_phone": "+23414401111",
                "support_email": "careng@dhl.com",
            },
            {
                "name": "GIG Logistics",
                "code": "gig",
                "description": "GIG Logistics - Nigerian courier service",
                "type": CarrierType.SCRAPER,
                "status": CarrierStatus.ACTIVE,
                # "requires_scraping": True,
                "scraper_config": {
                    "url": "https://giglogistics.com/track",
                    "selectors": {
                        "tracking_input": "input[name='tracking_number']",
                        "submit_button": "button[type='submit']",
                        "result_container": ".tracking-results",
                        "status": ".tracking-status",
                        "location": ".tracking-location",
                        "timestamp": ".tracking-time",
                    },
                    "requires_js": True,
                },
                "tracking_url_template": "https://giglogistics.com/track/{tracking_id}",
                "tracking_id_pattern": "^GIG\\d{8,10}$",
                "country": "Nigeria",
                "support_phone": "+2347000000000",
                "support_email": "info@giglogistics.com",
            },
            {
                "name": "NIPOST",
                "code": "nipost",
                "description": "Nigerian Postal Service",
                "type": CarrierType.SCRAPER,
                "status": CarrierStatus.ACTIVE,
                # "requires_scraping": True,
                "scraper_config": {
                    "url": "https://nipost.post/nipp/tracking.aspx",
                    "selectors": {
                        "tracking_input": "#txtTrack",
                        "submit_button": "#btnTrack",
                        "result_container": ".tracking-result",
                        "status": ".status",
                        "location": ".location",
                        "timestamp": ".timestamp",
                        "description": ".description",
                    },
                    "requires_js": False,
                },
                "tracking_url_template": "https://nipost.post/nipp/tracking.aspx?id={tracking_id}",
                "tracking_id_pattern": "^NP\\d{8,10}$",
                "country": "Nigeria",
                "support_phone": "+2347000000000",
                "support_email": "info@nipost.post",
            },
            {
                "name": "MAX.NG",
                "code": "max_ng",
                "description": "MAX Delivery Services",
                "type": CarrierType.SCRAPER,
                "status": CarrierStatus.ACTIVE,
                # "requires_scraping": True,
                "scraper_config": {
                    "url": "https://max.ng/track",
                    "selectors": {
                        "tracking_input": "input[type='text']",
                        "submit_button": "button[type='submit']",
                        "result_container": ".result-container",
                        "status": ".status-text",
                        "rider": ".rider-info",
                        "timestamp": ".time-stamp",
                    },
                    "requires_js": True,
                },
                "tracking_url_template": "https://max.ng/track/{tracking_id}",
                "tracking_id_pattern": "^MAX\\d{8}$",
                "country": "Nigeria",
                "support_phone": "+2347000000000",
                "support_email": "support@max.ng",
            },
            # Manual Input Carrier (for local riders)
            {
                "name": "Local Dispatch",
                "code": "local",
                "description": "Manual entry for local dispatch riders",
                "type": CarrierType.MANUAL,
                "status": CarrierStatus.ACTIVE,
                "country": "Nigeria",
            },
        ]

        for carrier_data in carriers:
            # Convert enums to their string values(e.g., CarrierType.API -> "api")
            if isinstance(carrier_data["type"], CarrierType):
                carrier_data["type"] = carrier_data["type"].value

            if isinstance(carrier_data["status"], CarrierStatus):
                carrier_data["status"] = carrier_data["status"].value

            carrier = Carrier(**carrier_data)
            db.add(carrier)
            logger.info(f"Added carrier: {carrier.name}")

        db.commit()
        logger.info(f"✅ Successfully seeded {len(carriers)} carriers to database")

    except Exception as e:
        logger.error(f"❌ Error seeding carriers: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_carriers()
