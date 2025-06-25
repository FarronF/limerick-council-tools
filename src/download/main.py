import argparse
from datetime import datetime
import urllib3
from typing import List

from src.download.get_meetings_from_website import get_public_meetings_for_year_month
from src.download.meeting_files_downloader import MeetingFilesDownloader
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        


def download_meeting_files(start_year: int, start_month: int, end_year: int, end_month: int, meeting_filter: List[str] = None, file_filter: List[str] = None, download_location: str = "./data/downloaded"):
    print(f"Fetching meeting minutes from {start_year}-{start_month} to {end_year}-{end_month}...")
    if meeting_filter:
        print(f"Filtering meetings by name containing: '{meeting_filter}' (case insensitive)")
    if file_filter:
        print(f"Filtering files by name containing: '{file_filter}' (case insensitive)")
    
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1) # Using first date will still include the entire month
    current_date = start_date
    downloader = MeetingFilesDownloader(destination_folder = download_location)
    

    while current_date <= end_date:
        meetings = get_public_meetings_for_year_month(current_date.year, current_date.month, meeting_filter)
        downloader.download_meeting_files_from_website(meetings, file_filter)
        current_date = _add_month(current_date)
    
    
def _add_month(date: datetime) -> datetime:
    """Add one month to the given date."""
    if date.month == 12:
        return date.replace(year=date.year + 1, month=1)
    else:
        return date.replace(month=date.month + 1)

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

    if not args.file_filter:  # If file-filter is provided with no arguments
        args.file_filter = None
        
    download_meeting_files(
        start_year=args.start_year,
        start_month=args.start_month,
        end_year=args.end_year,
        end_month=args.end_month,
        meeting_filter=args.meeting_filter,
        file_filter=args.file_filter,
    )