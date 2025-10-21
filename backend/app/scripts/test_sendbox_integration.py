"""
Test script for Sendbox API integration
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.carrier_connector.sendbox import SendboxConnector
from app.core.config import settings
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_sendbox_connector():
    """ "Test Sendbox connector with mock and real data"""

    print("Testing Sendbox Connector")
    print("=" * 40)

    # Initialize conncetor
    connector = SendboxConnector()

    # Check if API key is configured
    if not settings.SENDBOX_API_KEY:
        print("❌ SENDBOX_API_KEY not configured in settings. Skipping API test.")
        print("Get your API key from: https://app.sendbox.co/settings/developer")

        return False

    print(
        "✅ SENDBOX_API_KEY: {'*' * 10}{settings.SENDBOX_API_KEY[-4:]} is configured."
    )

    # Test tracking with different scenarios
    test_cases = [
        # (tracking_id, description)
        ("SBXDEMO12345", "Demo tracking ID"),
        ("SBXINVALID999", "Invalid tracking ID"),
        # # (description, method, tracking_id, expected_status)
        # (
        #     "Valid tracking ID via API",
        #     "api",
        #     "SBX1234567890",
        #     "in_transit",
        # ),
        # (
        #     "Invalid tracking ID format",
        #     "api",
        #     "INVALID123",
        #     "unknown",
        # ),
        # (
        #     "Webhook payload simulation",
        #     "webhook",
        #     {
        #         "tracking_id": "SBX1234567890",
        #         "status": "delivered",
        #         "location": "Lagos",
        #     },
        #     "delivered",
        # ),
        # (
        #     "Scraper fallback (simulated)",
        #     "scraper",
        #     "SBX0987654321",
        #     "pending",
        # ),
    ]

    successful_tests = 0

    for tracking_id, description in test_cases:
        print(f"\n Testing; {tracking_id} ({description})")
        print("-" * 40)

        try:
            result = connector.track(tracking_id)

            if result:
                print(f" Tracking Successful")
                print(f" Universal Status: {result.universal_status}")
                print(f"   Carrier Status: {result.carrier_status}")
                print(f"   Location: {result.location}")
                print(f"   Timestamp: {result.timestamp}")
                print(f"   Description: {result.description}")

                if result.coordinates:
                    print(f"   Coordinates: {result.coordinates}")

                successful_tests += 1
            else:
                print("❌ Tracking failed or returned no data.")

        except Exception as e:
            print(f"❌ Exception during tracking: {str(e)}")

    print("\n" + "=" * 40)
    print(f"Results: {successful_tests}/{len(test_cases)} tests passed")

    return successful_tests > 0


def test_sendbox_normalization():
    """Tests how raw Sendbox API responses are transformed into your internal data format (universal tracking schema)"""
    print("\nTesting Sendbox Data Normalization")
    print("=" * 40)

    connector = SendboxConnector()

    # Mock sendbox API response for testing
    mock_responses = [
        {
            "data": {
                "status": "pending",
                "status_description": "Package received at warehouse",
                "current_location": "Lagos Warehouse",
                "updated_at": "2024-01-15T10:30:00Z",
                "rider_name": "John Doe",
            }
        },
        {
            "data": {
                "status": "in_transit",
                "status_description": "Package in transit to destination",
                "current_location": "Ikeja Hub, Lagos",
                "updated_at": "2024-01-15T14:45:00Z",
                "rider_name": "Jane Smith",
                "latitude": "6.5244",
                "longitude": "3.3792",
            }
        },
        {
            "data": {
                "status": "delivered",
                "status_description": "Package delivered successfully",
                "current_location": "Victoria Island, Lagos",
                "updated_at": "2024-01-16T09:15:00Z",
                "rider_name": "Mike Johnson",
            }
        },
    ]

    for i, mock_data in enumerate(mock_responses, 1):
        print(f"\n Mock Dta Test {i}:")
        print("-" * 30)

        try:
            normalized_data = connector.normalize_data(mock_data)

            print(f" Normalization Successful")
            print(f"   Universal Status: {normalized_data.universal_status}")
            print(f"   Carrier Status: {normalized_data.carrier_status}")
            print(f"   Location: {normalized_data.location}")
            print(f"   City: {normalized_data.city}")
            print(f"   State: {normalized_data.state}")
            print(f"   Description: {normalized_data.description}")

        except Exception as e:
            print(f"Normalizaion error: {str(e)}")


def test_rate_limiting():
    """Test rate limiting functionality"""
    print("\n Testing Rate Limiting")
    print("=" * 40)

    connector = SendboxConnector()

    import time

    start_time = time.time()

    # Simulate multiple rapid requests
    for i in range(3):
        print(f"Request {i+1}...")
        connector.rate_limit()
        # Simulate a quick API call
        time.sleep(0.5)  # Simulate network delay

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Total time for 3 requests: {total_time:.2f} seconds")
    print(f"Minimum excepted time: {2 * connector.request_interval:.2f} seconds")

    if total_time >= (2 * connector.request_interval):
        print("✅ Rate limiting working as expected.")
    else:
        print("❌ Rate limiting not functioning correctly.")


if __name__ == "__main__":
    # Run all tests
    success = test_sendbox_connector()
    test_sendbox_normalization()
    test_rate_limiting()

    print("\n" + "=" * 40)
    if success:
        print("Sendbox Connector Tests Completed Successfully")
    else:
        print(
            "Sendbox Connector Tests Completed with Failures. Check your Sendbox API configuration"
        )
        print("\nNext steps:")
        print(
            "1. Ensure you have a valid Sendbox API key from https://app.sendbox.co/settings/developer"
        )
        print("2. Verify your tracking IDs are correct and exist in Sendbox")
