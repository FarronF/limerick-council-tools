import os
import glob
import fitz
import json
import argparse
from typing import List
from markdownify import markdownify as markdownify
from PIL import Image
import pytesseract
from datetime import datetime
import re
from urllib.parse import quote

# Record the script start time
script_start_time = datetime.now()

MEETING_README_TEMPLATE = """# Meeting Details

**Meeting Name:** {meeting_name}

**Date and Time:** {datetime}

**[Link to Meeting]({href})**

Files: 

"""

from typing import List

def process_meetings(start_year: int, start_month: int, end_year: int, end_month: int, meeting_filter: List[str] = None, file_filter: List[str] = None):
    """Processes PDFs, creates folder structure, and generates markdown files."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_folder = os.path.join(script_dir, "../data/meetings/downloaded")
    output_folder = os.path.join(script_dir, "../limerick-council-meetings/meetings")


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
                meeting_path = os.path.join(month_path, meeting_folder)
                if os.path.isdir(meeting_path) & (meeting_filter is None or any(filter_word.lower() in meeting_folder.lower() for filter_word in meeting_filter)):                                    
                    process_meeting(meeting_path, output_folder, file_filter)

def process_meeting(meeting_folder: str, output_folder: str, file_filter: List[str] = None):
    """Processes a single meeting folder and generates markdown files."""
    print(f"👥 Processing meeting: {meeting_folder}")
    meeting_details_path = os.path.join(meeting_folder, "meeting_details.json")
    if os.path.exists(meeting_details_path):
        with open(meeting_details_path, "r", encoding="utf-8") as details_file:
            meeting_details = json.load(details_file)
            relative_path = os.path.relpath(meeting_folder, "../data/meetings/downloaded")
            output_meeting_folder = os.path.join(output_folder, relative_path)

        if not os.path.exists(output_meeting_folder):
            os.makedirs(output_meeting_folder)

        # Create a README.md file content for the meeting
        readme_content = MEETING_README_TEMPLATE.format(
            meeting_name=meeting_details["meeting_name"],
            datetime=meeting_details["datetime"],
            href=meeting_details["href"]
        )
        

        files_info = meeting_details.get("files", [])
        if not files_info:
            readme_content += "No files available for this meeting."
    
        # Process PDFs in the meeting folder
        for file_info in files_info:
            file_name = file_info.get("file_name")
            display_text = file_info.get("display_text")
            file_url = file_info.get("url", "#")
            downloaded = file_info.get("downloaded")
            
            processed = False
            md_file_name = None
            
            if downloaded & (file_name.endswith(".pdf")) & (file_filter is None or any(filter_word.lower() in file_name.lower() for filter_word in file_filter)):
                pdf_file_path = os.path.join(meeting_folder, file_name)
                if os.path.exists(pdf_file_path):
                    processed = process_pdf(pdf_file_path, output_meeting_folder, file_url)
                    md_file_name = f"{os.path.splitext(os.path.basename(pdf_file_path))[0]}.md"
                else:
                    print(f"❌ File {pdf_file_path} not found, skipping PDF processing.")
            
            readme_content += f"{file_name} - [Original file]({file_url})"
            if processed and md_file_name:
                readme_content += f" - [Extracted text](./{quote(md_file_name)})"
            else:
                readme_content += " - Text not extracted"
            readme_content += "\n\n"
            
            readme_path = os.path.join(output_meeting_folder, "README.md")
            with open(readme_path, "w", encoding="utf-8") as readme_file:
                readme_file.write(readme_content)
            
def process_pdf(pdf_path, output_folder, original_url):
    """Processes a PDF with all methods and saves Markdown files."""
    print(f"📄 Processing PDF: {os.path.basename(pdf_path)}")
    try:
        markdown_output = process_with_markdownify(pdf_path)
        if markdown_output:
            markdown_output = f"[Original file]({original_url})\n\n---\n" + markdown_output
            save_markdown(markdown_output, pdf_path, output_folder)
        else:
            print(f"No content extracted from {pdf_path}.")
            return False
    except Exception as e:
        print(f"Error processing {pdf_path} with markdownify: {e}")
        return False
    return True


    
def process_with_markdownify(pdf_path):
    """Extracts text from a PDF using PyMuPDF and converts it to Markdown with markdownify.
    Includes OCR for scanned PDFs."""
    doc = fitz.open(pdf_path)
    markdown_output = ""
    ocr_used = False

    for page_num in range(len(doc)):
        page = doc[page_num]
        
        if not page.get_text().strip():  # If no text is found, use OCR
            if not ocr_used:
                log_ocr_usage(pdf_path)
                ocr_used = True
            pix = page.get_pixmap()  # Render page as an image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = img.resize((pix.width * 3, pix.height * 3), Image.Resampling.LANCZOS)
            ocr_text = pytesseract.image_to_string(img)
            
            markdown_output += f"*<small>Scanned page, text may contain errors. See original file for clarity</small>*  \n\n{ocr_text}\n"
        else:
            html_text = page.get_text("html")
            
            # Replace <img> tags with a placeholder
            html_text = re.sub(r'<img[^>]*>', '(Image omitted)', html_text)
            
            markdown_output += markdownify(html_text)
        markdown_output += "\n---\n"

    # Post-process the Markdown to remove redundant `****`
    markdown_output = re.sub(r'\*\*\*\*', '', markdown_output)

    return markdown_output


def save_markdown(markdown_content, pdf_path, output_folder):
    """Saves the Markdown content to a file with a method-specific suffix."""
    output_md_path = os.path.join(
        output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}.md"
    )
    with open(output_md_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

def log_ocr_usage(pdf_path):
    print(f"🔍 OCR used for {pdf_path}")
    # Generate the log file name based on the script start time
    log_file_name = f"{script_start_time.strftime('%Y-%m-%d_%H-%M-%S')}_ocr_usage.txt"
    log_file_path = os.path.join("../.log", log_file_name)
    
    os.makedirs("../.log", exist_ok=True)  # Ensure the logs folder exists
    with open(log_file_path, "a") as failed_file:
        failed_file.write(f"{pdf_path}\n")
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
    
    