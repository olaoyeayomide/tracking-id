from enum import Enum


class StatusEnum(str, Enum):
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    PENDING = "pending"
    FAILED = "failed"
