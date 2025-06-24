import argparse
from datetime import datetime
from src.download.download_meeting_files import download_meeting_files

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Download council meeting minutes PDFs.")
    parser.add_argument("--start-year", type=int, default=2014, help="Start year (e.g., 2023)")
    parser.add_argument("--start-month", type=int, default=1, help="Start month (1-12)")
    parser.add_argument("--end-year", type=int, default=datetime.now().year, help="End year (e.g., 2024)")
    parser.add_argument("--end-month", type=int, default=datetime.now().month, help="End month (1-12)")
    parser.add_argument("--meeting-filter", nargs='+', type=str, default=None, help="Filter meetings by names (case insensitive, e.g., 'council budget')")
    parser.add_argument("--file-filter", nargs='*', type=str, default=["agenda", "minutes"], help="Filter files by names (case insensitive, e.g., 'agenda minutes'). Use '--file-filter' with no arguments to disable filtering.")
    args = parser.parse_args()

    # Handle disabling file filter
    if not args.file_filter:  # If file-filter is provided with no arguments
        args.file_filter = None

    download_meeting_files(
        start_year=args.start_year,
        start_month=args.start_month,
        end_year=args.end_year,
        end_month=args.end_month,
        meeting_filter=args.meeting_filter,
        file_filter=args.file_filter
    )

