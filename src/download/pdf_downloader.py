import os
from pathlib import Path
import re

import requests


def download_pdf_to_folder(link: str, folder_path: Path):
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    url = link.get('href')
    
    link_text = str(link.string).strip() if link.string else "document"
    
    # Replace invalid characters in the filename
    safe_filename = re.sub(r'[\\/*?:"<>|]', "_", link_text) + ".pdf"
    
    file_path = os.path.join(folder_path, safe_filename)
    
    try:
        print(f"Downloading: {url} to {file_path}")
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        print(f"Downloaded: {file_path}")
    except Exception as e:
        print(f"\033[91m❌ Failed to download {url}: {e}\033[0m")
        return False
    return True