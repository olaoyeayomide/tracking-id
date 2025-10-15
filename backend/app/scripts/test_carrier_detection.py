"""
Test Script for carrier detection functionality
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.validators import validate_tracking_id
from app.database.connection import SessionLocal
from app.models.carrier import Carrier
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_carrier_detection():
    """ "Test tracking ID calidation and carrier detection"""

    # Test tracking IDs
    test_cases = [
        # (tracking_id, expected_carrier)
        ("SBX1234567890", "sendbox"),
        ("SBX-1234567890", "sendbox"),
        ("1234567890", "dhl"),
        ("12345678901", "dhl"),
        ("GIG12345678", "gig"),
        ("GIG-12345678", "gig"),
        ("NP12345678", "nipost"),
        ("NP-12345678", "nipost"),
        ("MAX12345678", "max_ng"),
        ("MAX-12345678", "max_ng"),
        ("1Z1234567890123456", "ups"),
        ("INVALID123", None),  # Should be valid format but unknown carrier
        ("ABC", None),  # Invalid - too short
    ]

    print("Testing Carrier Detection")
    print("=" * 40)

    successful_tests = 0
    total_tests = len(test_cases)

    for tracking_id, expected_carrier in test_cases:
        is_valid, detected_carrier = validate_tracking_id(tracking_id)

        status = "✅" if is_valid and detected_carrier == expected_carrier else "❌"

        print(
            f"{status} {tracking_id:20} -> Valid: {is_valid:5} | Carrie: {detected_carrier or 'Unknown':10} | Expected: {expected_carrier or 'Any':10}"
        )

        if is_valid and detected_carrier == expected_carrier:
            successful_tests += 1

    print("=" * 40)
    print(f"Results: { successful_tests}/{total_tests} test passed")

    # Test database carrier lookup
    print("\nTesting Carrier Lookup from Database")
    print("=" * 40)

    db = SessionLocal()
    try:
        carriers = db.query(Carrier).filter(Carrier.is_active == True).all()
        print(f"Active carriers in database: {len(carriers)}")

        # from carrier in carriers:
        #      status = "🟢" if carrier.status.value == "active" else "🟡"
        #      print(f"{status} { carrier.code:10} | {carrier.name:20} | Type: {carrier.type.value:10} | Webhook: {'Yes' if carrier.supports_webhook else 'No':3} | API: {'Yes' if carrier.supports_api else 'No':3} | Scraping: {'Yes' if carrier.requires_scraping else 'No':3}")

        for carrier in carriers:
            status = "🟢" if carrier.status.value == "active" else "🟡"
            print(
                f"{status} {carrier.code:10} | {carrier.name:20} | Type: {carrier.type.value:10} | Webhook: {carrier.webhook_verification}"
            )

    finally:
        db.close()


def test_tracking_patterns():
    """ "Test regex patterns for trackinG IDs"""
    print("\n Testing Tracking ID Patterns")
    print("=" * 40)

    patterns = {
        "sendbox": ["SBX1234567890", "SBX-1234567890", "sbx1234567890"],
        "dhl": ["1234567890", "12345678901", "123456789012"],
        "gig": ["GIG12345678", "GIG-12345678", "gig12345678"],
        "nipost": ["NP12345678", "NP-12345678", "np12345678"],
        "max_ng": ["MAX12345678", "MAX-12345678", "max12345678"],
    }

    for carrier, ids in patterns.items():
        print(f"\n{carrier.upper():10} Patterns:")
        for tracking_id in ids:
            is_valid, detected = validate_tracking_id(tracking_id)
            match = "✅" if detected == carrier else "❌"
            print(f"{ match} {tracking_id} -> Detected: {detected or 'Unknown':10}")


if __name__ == "__main__":
    test_carrier_detection()
    test_tracking_patterns()
