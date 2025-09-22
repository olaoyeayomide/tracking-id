from abc import ABC, abstractmethod
from typing import Dict, Any


class CarrierAdapter(ABC):
    """Abstract adapter each carrier should implement.
    Modes supported: webhook (push), api (pull), scraper, manual
    """

    name: str

    @abstractmethod
    async def fetch_by_api(self, tracking_id: str) -> Dict[str, Any]:
        """Fetch tracking info via carrier API."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_by_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch tracking info via carrier API."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_by_scraper(self, tracking_id: str) -> Dict[str, Any]:
        """Fetch tracking info via web scraping."""
        raise NotImplementedError
