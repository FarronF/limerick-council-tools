import json
import os
import re
import requests
from bs4 import BeautifulSoup
import argparse
from datetime import datetime, timedelta
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Record the script start time
script_start_time = datetime.now()
    
def fetch_web_content(url):
    try:
        # Make a GET request to fetch the content of the URL
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Return the content as text
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_calendar_html(response):
    parsed_response = json.loads(response)
    return parsed_response[3]["data"]
    
def get_public_meetings(html, filter_keywords=None):
    # Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")
    
    meeting_details = []
    
    # Example: Extract specific data, e.g., all links
    for item in soup.find_all('div', class_='view-item'):
        
        link_tag = item.find(
            'a', 
            string=lambda text: text and not text.strip().startswith("PRIVATE"),
            href=lambda href: href and href.startswith("/council/whats-on"))
        time_tag = item.find('time', class_='datetime')

        if link_tag and time_tag:
            meeting_name = link_tag.contents[0].strip()
            if not filter_keywords or any(keyword.lower() in meeting_name.lower() for keyword in filter_keywords):
                meeting_details.append({
                    'meeting_name': meeting_name,
                    'href': f"https://www.limerick.ie{link_tag['href']}",
                    'datetime': datetime.strptime(time_tag['datetime'], "%Y-%m-%dT%H:%M:%SZ")
                })
                print(meeting_name, link_tag['href'], time_tag['datetime'])
    
    return meeting_details
def handle_meetings(meetings, file_filters=None):
    
    prefix = "https://www.limerick.ie"
    for meeting in meetings:
        datetime = meeting['datetime']
        folder_name = re.sub(r'[\\/*?:"<>|]', "_", meeting['meeting_name'])
        folder_path = f"../data/meetings/downloaded/{datetime.year}/{datetime.month:02d}/{datetime.day:02d}-{folder_name}"
        os.makedirs(folder_path, exist_ok=True)
        
        json_file_path = os.path.join(folder_path, "meeting_details.json")
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(meeting, json_file, indent=4, default=str)
        
        # suffix = meeting['href']
        
        # url = f"{prefix}{suffix}"
        response = requests.get(meeting['href'], verify=False)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        links = soup.find_all(
            'a',
            string=lambda text: text and (not file_filters or any(keyword in text.strip().lower() for keyword in file_filters)),
            href=lambda href: href and href.endswith(".pdf"),
        )
        
        print(f"Found {len(links)} PDF links for {meeting['meeting_name']}:")
        
        download_pdfs_to_folder(links, folder_path)


def download_pdfs_to_folder(links, folder_path):
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    for link in links:
        url = link.get('href')
        
        # Get the text content of the link for the filename
        link_text = str(link.string).strip() if link.string else "document"
        
        # Replace invalid characters in the filename
        safe_filename = re.sub(r'[\\/*?:"<>|]', "_", link_text) + ".pdf"
        
        # Full path for the file
        file_path = os.path.join(folder_path, safe_filename)
        
        try:
            # Download the PDF
            print(f"Downloading: {url} to {file_path}")
            response = requests.get(url, stream=True, verify=False)
            response.raise_for_status()  # Raise an error for bad HTTP responses
            
            # Write the PDF to the file
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            
            print(f"Downloaded: {file_path}")
        except Exception as e:
            print(f"\033[91m❌ Failed to download {url}: {e}\033[0m")
            log_failed_download(folder_path, url)


# Function to log failed downloads
def log_failed_download(folder_path, failed_download):
    # Generate the log file name based on the script start time
    log_file_name = f"{script_start_time.strftime('%Y-%m-%d_%H-%M-%S')}_failed_downloads.txt"
    log_file_path = os.path.join("../.log", log_file_name)
    
    os.makedirs(".log", exist_ok=True)  # Ensure the logs folder exists
    with open(log_file_path, "a") as failed_file:
        failed_file.write(f"{folder_path}, {failed_download}\n")


# Example usage
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

    print(f"Fetching meeting minutes from {args.start_year}-{args.start_month} to {args.end_year}-{args.end_month}...")
    if args.meeting_filter:
        print(f"Filtering meetings by name containing: '{args.meeting_filter}' (case insensitive)")
    if args.file_filter:
        print(f"Filtering files by name containing: '{args.file_filter}' (case insensitive)")

    # Generate a list of months between start and end dates
    start_date = datetime(args.start_year, args.start_month, 1)
    end_date = datetime(args.end_year, args.end_month, 1)
    current_date = start_date

    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        url = f"https://www.limerick.ie/views/ajax?view_name=council_meetings_calendar&view_display_id=page_month&view_args={year}{month:02d}"
        print(f"Fetching data for {year}-{month:02d}...")
        content = fetch_web_content(url)

        if content:
            html = get_calendar_html(content)
            meetings = get_public_meetings(html, args.meeting_filter)
            
            print(f"Found {len(meetings)} meetings for {year}-{month:02d}.")
            handle_meetings(meetings, args.file_filter)

        # Move to the next month
        current_date += timedelta(days=31)
        current_date = current_date.replace(day=1)
