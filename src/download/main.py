from datetime import datetime
import urllib3
from typing import List

from src.download.get_meetings_from_website import get_public_meetings_for_year_month
from src.download.meeting_files_downloader import MeetingFilesDownloader
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        


def download_meeting_files(start_year: int, start_month: int, end_year: int, end_month: int, meeting_filter: List[str] = None, file_filter: List[str] = None):
    script_start_time = datetime.now()
    print(f"Fetching meeting minutes from {start_year}-{start_month} to {end_year}-{end_month}...")
    if meeting_filter:
        print(f"Filtering meetings by name containing: '{meeting_filter}' (case insensitive)")
    if file_filter:
        print(f"Filtering files by name containing: '{file_filter}' (case insensitive)")
    
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1) # Using first date will still include the entire month
    current_date = start_date
    downloader = MeetingFilesDownloader(destination_folder = "./data/meetings/downloaded", log_file_folder=".logs", log_file_name=f"{script_start_time.strftime('%Y-%m-%d_%H-%M-%S')}_failed_downloads.txt")
    

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
