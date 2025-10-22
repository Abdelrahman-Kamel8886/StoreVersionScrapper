from typing import Dict

class HistoryModel:
    def __init__(self,version: str,date: str):
        self.version = version
        self.date = date

    def to_dict(self) -> Dict[str, str]:
        """Convert HistoryModel to dictionary."""
        return {"version": self.version, "date": self.date}

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        """Create HistoryModel from dictionary."""
        return cls(version=data.get("version", ""), date=data.get("date", ""))
