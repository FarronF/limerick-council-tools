import os
import glob
import fitz
import json
from markdownify import markdownify as md
from PIL import Image
import pytesseract
from datetime import datetime
import re
from urllib.parse import quote  # Add this import at the top of the file

# Record the script start time
script_start_time = datetime.now()

# Define the template as a separate variable
README_TEMPLATE = """# Meeting Details

**Meeting Name:** {meeting_name}

**Date and Time:** {datetime}

**[Link to Meeting]({href})**

Files: 

"""

def process_meetings(input_folder, output_folder):
    """Processes PDFs, creates folder structure, and generates markdown files."""
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for year_folder in sorted(os.listdir(input_folder)):
        
        year_path = os.path.join(input_folder, year_folder)
        if os.path.isdir(year_path):
            for month_folder in sorted(os.listdir(year_path)):
                month_path = os.path.join(year_path, month_folder)
                if os.path.isdir(month_path):
                    for meeting_folder in sorted(os.listdir(month_path)):
                        meeting_path = os.path.join(month_path, meeting_folder)
                        if os.path.isdir(meeting_path):
                            process_meeting(meeting_path, output_folder)

def process_meeting(meeting_folder, output_folder):
    """Processes a single meeting folder and generates markdown files."""
    print(f"👥 Processing meeting: {meeting_folder}")
    meeting_details_path = os.path.join(meeting_folder, "meeting_details.json")
    if os.path.exists(meeting_details_path):
        with open(meeting_details_path, "r", encoding="utf-8") as details_file:
            meeting_details = json.load(details_file)
            relative_path = os.path.relpath(meeting_folder, input_folder)
            output_meeting_folder = os.path.join(output_folder, relative_path)

        if not os.path.exists(output_meeting_folder):
            os.makedirs(output_meeting_folder)

        # Create a README.md file content for the meeting
        readme_content = README_TEMPLATE.format(
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
            
            if downloaded:
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
            img = img.resize((pix.width * 3, pix.height * 3), Image.Resampling.LANCZOS)  # Resize image to 3x the size
            ocr_text = pytesseract.image_to_string(img)
            
            markdown_output += f"*<small>Scanned page, text may contain errors. See original file for clarity</small>*  \n{ocr_text}\n"
        else:
            html_text = page.get_text("html")  # Extract as HTML
            
            # Replace <img> tags with a placeholder
            html_text = re.sub(r'<img[^>]*>', '(Image omitted)', html_text)
            
            markdown_output += md(html_text)
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

# Function to log failed downloads
def log_ocr_usage(pdf_path):
    print(f"🔍 OCR used for {pdf_path}")
    # Generate the log file name based on the script start time
    log_file_name = f"{script_start_time.strftime('%Y-%m-%d_%H-%M-%S')}_ocr_usage.txt"
    log_file_path = os.path.join("../.log", log_file_name)
    
    os.makedirs(".log", exist_ok=True)  # Ensure the logs folder exists
    with open(log_file_path, "a") as failed_file:
        failed_file.write(f"{pdf_path}\n")

input_folder = "../data/meetings/downloaded"
output_folder = "../data/meetings/processed"