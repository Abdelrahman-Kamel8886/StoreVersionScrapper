from repository.repository import merge_all_apps
from utils.file_manger import export_json_file

def main():
   result = merge_all_apps()
   export_json_file(result.to_dict())



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram stopped by user")
    except Exception as e:
        print(f"\nProgram error: {str(e)}")