from datetime import datetime


def convert_timestamp_to_date(timestamp):
    """Convert Unix timestamp to readable date format"""
    try:
        if timestamp and timestamp != 'N/A':
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        return 'N/A'
    except (ValueError, TypeError, OSError):
        return 'N/A'

def convert_iso_to_date(iso_str: str) -> str:
    """
    Convert ISO datetime string like '2025-10-07T04:55:44Z' to '2025-10-07'.
    Returns 'N/A' if conversion fails.
    """
    try:
        # Handle both Zulu time and offset-free ISO formats
        if iso_str.endswith("Z"):
            iso_str = iso_str.replace("Z", "+00:00")

        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return "N/A"