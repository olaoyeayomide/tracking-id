from app.services.carrier_connector.sendbox import SendboxConnector
from app.services.carrier_connector.gig import GigConnector

CONNECTORS = {
    "SENDBOX": SendboxConnector,
    "GIG": GigConnector,
}


def get_connector(code: str, meta: dict | None = None):
    connector_cls = CONNECTORS.get(code.upper())
    if not connector_cls:
        raise ValueError(f"Unsupported carrier: {code}")
    return connector_cls(meta=meta)
