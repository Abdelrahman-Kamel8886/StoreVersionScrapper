import json
from datetime import datetime
from typing import List, Dict, Any

from model.app_model import AppData


class ScrapeResult:
    def __init__(
        self,
        scrape_date: str,
        total_apps: int,
        android_apps_count: int,
        ios_apps_count: int,
        android: List[AppData],
        ios: List[AppData]
    ):
        self.scrape_date = scrape_date
        self.total_apps = total_apps
        self.android_apps_count = android_apps_count
        self.ios_apps_count = ios_apps_count
        self.android = android
        self.ios = ios

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scrape_date": self.scrape_date,
            "total_apps": self.total_apps,
            "android_apps_count": self.android_apps_count,
            "ios_apps_count": self.ios_apps_count,
            "android": [app.to_dict() for app in self.android],
            "ios": [app.to_dict() for app in self.ios],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScrapeResult":
        android_data = [AppData.from_dict(d) for d in data.get("android", [])]
        ios_data = [AppData.from_dict(d) for d in data.get("ios", [])]

        return cls(
            scrape_date=data.get("scrape_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            total_apps=data.get("total_apps", 0),
            android_apps_count=data.get("android_apps_count", len(android_data)),
            ios_apps_count=data.get("ios_apps_count", len(ios_data)),
            android=android_data,
            ios=ios_data,
        )

    @classmethod
    def from_json(cls, json_str: str) -> "ScrapeResult":
        return cls.from_dict(json.loads(json_str))
