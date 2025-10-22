from datetime import datetime
import requests
from google_play_scraper import app
from model.app_model import AppData
from model.bank_model import BankModel
from model.history_model import HistoryModel
from utils import constans as const
from utils.date_manger import convert_timestamp_to_date, convert_iso_to_date


def fetch_android_app_data(bank : BankModel):
    """Fetch app model from Google Play Store"""
    try:
        result = app(
            bank.androidId,
            lang='en',
            country='eg'
        )

        app_data = AppData(
            bank_name=bank.bankName,
            app_id = bank.androidId,
            platform = const.android_type,
            app_name = result.get('title', 'N/A'),
            version = result.get('version', 'N/A'),
            release_date = convert_timestamp_to_date(result.get('updated')),
            rate=result.get('score', 'N/A'),
            last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            image_url=result.get('icon', 'N/A'),
            store_url=result.get('url', 'N/A'),
            history = [
                HistoryModel(
                    version = result.get('version', 'N/A'),
                    date = convert_timestamp_to_date(result.get('updated')),
                )
            ]
        )

        return app_data

    except Exception as e:
        print(f"Error fetching model for {bank.bankName}: {str(e)}")
        return {
            "app_id": bank.androidId,
            "platform": "Android",
            "error": str(e),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def fetch_ios_app_data(bank: BankModel):
    """Fetch app model from iOS App Store using iTunes API."""
    try:
        url = f"https://itunes.apple.com/lookup?country=eg&id={bank.iosId}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        if data.get('resultCount', 0) > 0:
            result = data['results'][0]

            # create AppData model
            app_data = AppData(
                bank_name=bank.bankName,
                app_id=bank.iosId,
                platform=const.ios_type,
                app_name=result.get('trackName', 'N/A'),
                version=result.get('version', 'N/A'),
                release_date=
                convert_iso_to_date(result.get('currentVersionReleaseDate', 'N/A')),
                rate=result.get('averageUserRating', 'N/A'),
                last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                image_url=result.get('artworkUrl100', 'N/A'),
                store_url=result.get('trackViewUrl', 'N/A'),
                history=[
                    HistoryModel(
                        version=result.get('version', 'N/A'),
                        date=
                            convert_iso_to_date(result.get('currentVersionReleaseDate', 'N/A'))
                    )
                ],
            )

            return app_data

        else:
            return {
                "app_id": bank.iosId,
                "platform": const.ios_type,
                "error": "App not found in iTunes Store",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

    except requests.exceptions.RequestException as e:
        print(f"Network error fetching iOS model for {bank.bankName}: {str(e)}")
        return {
            "app_id": bank.iosId,
            "platform": const.ios_type,
            "error": f"Network error: {str(e)}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    except Exception as e:
        print(f"Error fetching iOS model for {bank.bankName}: {str(e)}")
        return {
            "app_id": bank.iosId,
            "platform": const.ios_type,
            "error": str(e),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

