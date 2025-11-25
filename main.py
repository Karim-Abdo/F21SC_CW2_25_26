import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analytics_manager import AnalyticsManager
from config import DEFAULT_DATA_FILE


def main():
    if len(sys.argv) > 1:
        # Create manager with no file path (CLI will set file path)
        analytics = AnalyticsManager()
        analytics.run_cli()
        return

    # Otherwise run GUI mode and prompt for a data file
    print("Document Tracker Analytics (GUI mode)")
    print("Default data file:", DEFAULT_DATA_FILE)

    file_path = input(f"Enter path to JSON data file (or press Enter for default): ").strip()
    if not file_path:
        file_path = DEFAULT_DATA_FILE

    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} does not exist.", file=sys.stderr)
        print("Please make sure the data file is in the correct location.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return

    analytics = AnalyticsManager(file_path)
    analytics.run_gui()


if __name__ == "__main__":
    main()
