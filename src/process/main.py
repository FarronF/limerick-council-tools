import os
import argparse
from typing import List
from datetime import datetime
from urllib.parse import quote

# Record the script start time
script_start_time = datetime.now()
from src.process.meeting_processor import MeetingProcessor

from typing import List

def process_meetings(start_year: int, start_month: int, end_year: int, end_month: int, meeting_filter: List[str] = None, file_filter: List[str] = None, download_location: str = "./data/meetings/downloaded", output_location: str = "./limerick-council-meetings/meetings"):
    """Processes PDFs, creates folder structure, and generates markdown files."""
    
    input_folder = os.path.abspath(os.path.join(download_location))
    output_folder = os.path.abspath(os.path.join(output_location))
    
    meeting_processor = MeetingProcessor()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    for year in range(start_year, end_year + 1):
        year_path = os.path.join(input_folder, str(year))
        if not os.path.exists(year_path):
            print(f"Year folder {year_path} does not exist, skipping year {year}.")
            continue
        
        if year == start_year:
            start_month_range = start_month
        else:
            start_month_range = 1
            
        if year == end_year:
            end_month_range = end_month
        else:
            end_month_range = 12

        for month in range(start_month_range, end_month_range + 1):
            month_folder = f"{month:02d}"
            month_path = os.path.join(year_path, month_folder)
            if not os.path.exists(month_path):
                print(f"Month folder {month_path} does not exist, skipping month {month}.")
                continue
            for meeting_folder in sorted(os.listdir(month_path)):
                meeting_folder_path = os.path.join(month_path, meeting_folder)
                output_meeting_folder = os.path.join(output_folder, str(year), month_folder, meeting_folder)
                if os.path.isdir(meeting_folder_path) & (meeting_filter is None or any(filter_word.lower() in meeting_folder.lower() for filter_word in meeting_filter)):                                    
                    meeting_processor.process_meeting(meeting_folder_path, output_meeting_folder, file_filter)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Parse council meeting minutes PDFs to markdown.")
    parser.add_argument("--start-year", type=int, default=2014, help="Start year (e.g., 2023)")
    parser.add_argument("--start-month", type=int, default=1, help="Start month (1-12)")
    parser.add_argument("--end-year", type=int, default=datetime.now().year, help="End year (e.g., 2024)")
    parser.add_argument("--end-month", type=int, default=datetime.now().month, help="End month (1-12)")
    parser.add_argument("--meeting-filter", nargs='+', type=str, default=None, help="Filter meetings by names (case insensitive, e.g., 'council budget')")
    parser.add_argument("--file-filter", nargs='*', type=str, default=None, help="Filter files by names (case insensitive, e.g., 'agenda minutes'). Use '--file-filter' with no arguments to disable filtering.")
    args = parser.parse_args()
    
    process_meetings(args.start_year, args.start_month, args.end_year, args.end_month, args.meeting_filter, args.file_filter)
    
    