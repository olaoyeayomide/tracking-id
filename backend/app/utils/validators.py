import re
from typing import Optional, Tuple
from datetime import datetime


def validate_tracking_id(tracking_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validate tracking ID format and identify carrier.
    Returns (is_valid, carrier_name) tuple.
    """
    if not tracking_id or len(tracking_id) < 5:
        return False, "Tracking ID too short"

    # Carrier-specific patterns
    patterns = {
        "sendbox": r"^SBX[-]?\d{10}$",
        "dhl": r"^[-]?\d{10,11}$",
        "fedex": r"^[-]?\d{12,20}$",
        "ups": r"^1Z[A-Z0-9]{16}$",
        "gig": r"^GIG[-]?\d{8,10}$",
        "nipost": r"^NP[-]?\d{8,10}$",
        "kwik": r"^KWIK[-]?\d{6,8}$",
        "max_ng": r"^MAX[-]?\d{8,10}$",
    }

    for carrier, pattern in patterns.items():
        if re.match(pattern, tracking_id.upper()):
            return True, carrier
    return True, None  # Valid but unknown carrier
