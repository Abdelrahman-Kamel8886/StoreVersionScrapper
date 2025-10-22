import json
import os

from model.scrape_result import ScrapeResult
from utils.constans import output_file_name


def export_json_file(json_data, filename=output_file_name):
    """
    Save JSON data to a file inside /output folder.
    Creates folder if not exists.
    """
    try:
        # create folder if not exists
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)

        # full file path
        file_path = os.path.join(output_dir, filename)

        # write JSON data
        with open(file_path, "w", encoding="utf-8") as f:
            if isinstance(json_data, (dict, list)):
                json.dump(json_data, f, indent=4, ensure_ascii=False)
            elif isinstance(json_data, str):
                # if already a JSON string
                f.write(json_data)
            else:
                raise TypeError("json_data must be dict, list, or JSON string")

        print(f"✅ JSON saved to {file_path}")

        return file_path

    except Exception as e:
        print(f"❌ Failed to save JSON: {str(e)}")
        return None

def read_json_file(filename=output_file_name) -> ScrapeResult | None:
    """
    Reads a JSON file from /output folder and converts it to a ScrapeResult object.
    Returns None if file not found or invalid.
    """
    try:
        output_dir = os.path.join(os.getcwd(), "output")
        file_path = os.path.join(output_dir, filename)

        if not os.path.exists(file_path):
            print(f"⚠️ File not found: {file_path}")
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # Convert the loaded data into a ScrapeResult instance
        scrape_result = ScrapeResult.from_dict(json_data)
        print(f"✅ Loaded JSON from {file_path}")
        return scrape_result

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Failed to read JSON file: {str(e)}")
        return None
