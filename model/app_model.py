import json
from typing import List, Dict

from model.history_model import HistoryModel


class AppData:
    def __init__(
            self,
            app_id: str,
            platform: str,
            app_name: str,
            version: str,
            release_date: str,
            rate: str,
            last_updated: str,
            image_url: str,
            store_url: str,
            history: List[HistoryModel],
    ):
        self.app_id = app_id
        self.platform = platform
        self.app_name = app_name
        self.version = version
        self.release_date = release_date
        self.rate = rate
        self.last_updated = last_updated
        self.image_url = image_url
        self.store_url = store_url
        self.history = history

    def to_dict(self) -> Dict:
        """Convert AppData (with history) to dictionary."""
        return {
            "app_id": self.app_id,
            "platform": self.platform,
            "app_name": self.app_name,
            "version": self.version,
            "release_date": self.release_date,
            "rate": self.rate,
            "last_updated": self.last_updated,
            "image_url": self.image_url,
            "store_url": self.store_url,
            "history": [h.to_dict() for h in self.history],
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict):
        """Create AppData from a dict."""
        history_data = data.get("history", [])
        history_models = [HistoryModel.from_dict(h) for h in history_data]
        return cls(
            app_id=data.get("app_id", "N/A"),
            platform=data.get("platform", "Unknown"),
            app_name=data.get("app_name", "N/A"),
            version=data.get("version"),
            release_date=data.get("release_date"),
            rate=data.get("rate"),
            last_updated=data.get("last_updated"),
            image_url=data.get("image_url", "N/A"),
            store_url=data.get("store_url"),
            history=history_models,
        )

    @classmethod
    def from_json(cls, json_str: str):
        """Create AppData from JSON string."""
        return cls.from_dict(json.loads(json_str))

    @staticmethod
    def list_to_json(apps: List["AppData"], indent: int = 2) -> str:
        """Convert list of AppData objects to JSON string."""
        return json.dumps([a.to_dict() for a in apps], indent=indent)

    @staticmethod
    def list_from_json(json_str: str) -> List["AppData"]:
        """Convert JSON array string to list of AppData."""
        data = json.loads(json_str)
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array")
        return [AppData.from_dict(d) for d in data]
