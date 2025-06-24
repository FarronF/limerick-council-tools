import json
import os
import re
from pathlib import Path
from typing import List
from bs4 import BeautifulSoup
from src.download.fetch_web_content import fetch_web_content
from src.download.pdf_downloader import download_pdf_to_folder
from src.types.meeting_details import MeetingDetails

class MeetingFilesDownloader:
    def __init__(self, destination_folder: str = None, log_file_folder: str = None, log_file_name: str = 'log.txt'):
        self.destination_folder = Path(destination_folder) if destination_folder else Path.cwd() / 'data/meetings'
        self.log_file_path = Path(log_file_folder) if log_file_folder else Path.cwd() / '.log' / log_file_name

    def download_meeting_files_from_website(self, meetings: List[MeetingDetails], file_filters: List[str] = None):
        print(meetings)
        if(meetings is None or len(meetings) == 0):
            return
        print(f"Files will be downloaded to: {self.destination_folder}")
        print(f"Log file will be saved to: {self.log_file_path}")
        for meeting in meetings:
            datetime = meeting['datetime']
            folder_name = re.sub(r'[\\/*?:"<>|]', "_", meeting['meeting_name'])
            destination_path = Path(self.destination_folder) / f"{datetime.year}" / f"{datetime.month:02d}" / f"{datetime.day:02d}-{folder_name}"
            os.makedirs(destination_path, exist_ok=True)
            
            meeting_page_html = fetch_web_content(meeting['href'])
            
            
            soup = BeautifulSoup(meeting_page_html, "html.parser")
            
            links = soup.find_all(
                'a',
                href=lambda href: href and href.endswith(".pdf"),
            )
            
            files = []
            for link in links:
                display_text = link.string.strip() if link.string else "document"
                file_name = re.sub(r'[\\/*?:"<>|]', "_", display_text) + ".pdf"
                
                file = {
                    'display_text': display_text,
                    'file_name': file_name,
                    'url': link.get('href'),
                    'downloaded': False
                }
                
                if not file_filters or any(filter_word.lower() in file_name.lower() for filter_word in file_filters):
                    download_success = download_pdf_to_folder(link, destination_path)
                    file['downloaded'] = download_success
                    if(not download_success):
                        self._log_failed_download(destination_path, file['url'])

                print(f"File: {file}")
                files.append(file)
            
            meeting['files'] = files
            json_file_path = os.path.join(destination_path, "meeting_details.json")
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(meeting, json_file, indent=4, default=str)

    def _log_failed_download(folder_path, failed_download):
        log_file_name = f"{script_start_time.strftime('%Y-%m-%d_%H-%M-%S')}_failed_downloads.txt"
        log_file_path = os.path.join("../.log", log_file_name)
        
        os.makedirs("../.log", exist_ok=True)  # Ensure the logs folder exists
        with open(log_file_path, "a") as failed_file:
            failed_file.write(f"{folder_path}, {failed_download}\n")