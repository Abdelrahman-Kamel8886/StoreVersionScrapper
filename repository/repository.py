from datetime import datetime

from data.bank_list import android_ids, ios_ids
from model.scrape_result import ScrapeResult
from remote.remote_data_source import fetch_android_app_data, fetch_ios_app_data
from utils.file_manger import read_json_file


def scrape_all_apps():
    """Scrape model for all apps and save to JSON"""
    print(f"Starting model scraping at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    android_data = []
    ios_data = []

    # Fetch Android apps model
    print("Fetching Android apps model...")
    for app_id in android_ids:
        print(f"Fetching Android model for: {app_id}")
        data = fetch_android_app_data(app_id)
        android_data.append(data)

    # Fetch iOS apps model
    print("Fetching iOS apps model...")
    for app_id in ios_ids:
        print(f"Fetching iOS model for: {app_id}")
        data = fetch_ios_app_data(app_id)
        ios_data.append(data)

    final_data = ScrapeResult(
        scrape_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        total_apps= len(android_data) + len(ios_data),
        android_apps_count= len(android_data),
        ios_apps_count= len(ios_data),
        android=android_data,
        ios=ios_data
    )

    return final_data

def merge_all_apps() -> ScrapeResult:
    """
    Merge newly scraped app data with old saved data.
    Updates versions, history, and last_updated for changed apps.
    Adds any new apps that were not previously saved.
    """
    new_data = scrape_all_apps()
    old_data = read_json_file()

    # If no previous data, just return new data
    if old_data is None:
        return new_data

    def merge_platform_data(new_list, old_list):
        """Helper function to merge apps for a single platform."""
        # Create dictionary for quick lookup of old apps by ID
        old_dict = {app.app_id: app for app in old_list}

        for new_app in new_list:
            existing_app = old_dict.get(new_app.app_id)

            if existing_app:
                # Check if version/release changed
                if existing_app.version != new_app.version:
                    existing_app.history.append(new_app.history[0])
                    existing_app.version = new_app.version
                    existing_app.release_date = new_app.release_date

                # Always update last_updated timestamp
                existing_app.last_updated = new_app.last_updated
            else:
                # Add new app if not found
                old_list.append(new_app)

        return old_list

    # Merge Android and iOS apps using helper
    old_data.android = merge_platform_data(new_data.android, old_data.android)
    old_data.ios = merge_platform_data(new_data.ios, old_data.ios)

    # Recalculate counts and totals
    old_data.total_apps = len(old_data.android) + len(old_data.ios)
    old_data.android_apps_count = len(old_data.android)
    old_data.ios_apps_count = len(old_data.ios)
    old_data.scrape_date = new_data.scrape_date

    return old_data