# backend/scripts/test_tracking_validation.py

# Test the tracking ID validation
from app.utils.validators import validate_tracking_id

test_ids = ["SBX1234567890", "1234567890", "NP12345678", "GIG123456"]

for tracking_id in test_ids:
    is_valid, carrier = validate_tracking_id(tracking_id)
    print(f"{tracking_id} -> Valid: {is_valid}, Carrier: {carrier}")
