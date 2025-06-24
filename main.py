import argparse
from datetime import datetime
from src.download.main import download_meeting_files
from src.process.main import process_meetings

if __name__ == "__main__":
    script_start_time = datetime.now()
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Download council meeting minutes PDFs.")
    parser.add_argument("--start-year", type=int, default=2014, help="Start year (e.g., 2023)")
    parser.add_argument("--start-month", type=int, default=1, help="Start month (1-12)")
    parser.add_argument("--end-year", type=int, default=datetime.now().year, help="End year (e.g., 2024)")
    parser.add_argument("--end-month", type=int, default=datetime.now().month, help="End month (1-12)")
    parser.add_argument("--meeting-filter", nargs='+', type=str, default=None, help="Filter meetings by names (case insensitive, e.g., 'council budget')")
    parser.add_argument("--file-filter", nargs='*', type=str, default=["agenda", "minutes"], help="Filter files by names (case insensitive, e.g., 'agenda minutes'). Use '--file-filter' with no arguments to disable filtering.")
    parser.add_argument("--download-location", type=str, default="./data/meetings/downloaded", help="Location to save downloaded files")
    parser.add_argument("--output-location", type=str, default="./limerick-council-meetings/meetings", help="Location to output processed markdown files")
    parser.add_argument("--logs-location", type=str, default="./.logs", help="Location to output logs")
    parser.add_argument("--dont-download", action="store_true", help="Do no download new files, process existing files only")
    parser.add_argument("--dont-process", action="store_true", help="Do not process files to markdown")
    parser.add_argument("--delete-downloads-after-complete", action="store_true", help="Delete downloaded files after processing")
    args = parser.parse_args()

    # Handle disabling file filter
    if not args.file_filter:  # If file-filter is provided with no arguments
        args.file_filter = None

    if(not args.dont_download):        
        download_meeting_files(
            start_year=args.start_year,
            start_month=args.start_month,
            end_year=args.end_year,
            end_month=args.end_month,
            meeting_filter=args.meeting_filter,
            file_filter=args.file_filter,
            download_location=args.download_location,
            log_file_folder=args.logs_location,
            log_file_prefix=f"{script_start_time.strftime('%Y-%m-%d_%H-%M-%S')}"
        )
        
    if(not args.dont_process):        
        process_meetings(
            start_year=args.start_year,
            start_month=args.start_month,
            end_year=args.end_year,
            end_month=args.end_month,
            meeting_filter=args.meeting_filter,
            file_filter=args.file_filter,
            download_location=args.download_location,
            output_location=args.output_location,
            log_file_folder=args.logs_location,
            log_file_prefix=f"{script_start_time.strftime('%Y-%m-%d_%H-%M-%S')}"
        )

    if(args.delete_downloads_after_complete):
        import shutil
        import os
        if os.path.exists(args.download_location):
            print(f"Removing download location {args.download_location}")
            shutil.rmtree(args.download_location)
        else:
            print(f"Download location {args.download_location} does not exist, skipping deletion.")