import os
import glob
import fitz
import json
from markdownify import markdownify as md
import pdfplumber
import pypandoc
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from marker.config.parser import ConfigParser
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pdfminer")
# import torch

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define the template as a separate variable
README_TEMPLATE = """# Meeting Details

**Meeting Name:** {meeting_name}

**Date and Time:** {datetime}

**Link to Meeting:** [Original Meeting Details]({href})
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
    meeting_details_path = os.path.join(meeting_folder, "meeting_details.json")
    if os.path.exists(meeting_details_path):
        with open(meeting_details_path, "r", encoding="utf-8") as details_file:
            meeting_details = json.load(details_file)
            relative_path = os.path.relpath(meeting_folder, input_folder)
            output_meeting_folder = os.path.join(output_folder, relative_path)

        if not os.path.exists(output_meeting_folder):
            os.makedirs(output_meeting_folder)

        # Process PDFs in the meeting folder
        for pdf_file in glob.glob(os.path.join(meeting_folder, "*.pdf")):
            process_pdf_with_all_methods(pdf_file, output_meeting_folder)

def process_pdf_with_all_methods(pdf_path, output_folder):
    """Processes a PDF with all methods and saves Markdown files."""
    try:
        # Method 1: pdfplumber
        # try:
        #     markdown_output = process_with_pdfplumber(pdf_path)
        #     save_markdown(markdown_output, pdf_path, output_folder, "pdfplumber")
        # except Exception as e:
        #     print(f"Error processing {pdf_path} with pdfplumber: {e}")

        # # Method 2: pypandoc
        # # try:
        # #     markdown_output = pypandoc.convert_file(pdf_path, "markdown")
        # #     save_markdown(markdown_output, pdf_path, output_folder, "pypandoc")
        # # except Exception as e:
        # #     print(f"Error processing {pdf_path} with pypandoc: {e}")

        # # Method 3: markdownify with PyMuPDF
        # try:
        #     markdown_output = process_with_markdownify(pdf_path)
        #     save_markdown(markdown_output, pdf_path, output_folder, "markdownify")
        # except Exception as e:
        #     print(f"Error processing {pdf_path} with markdownify: {e}")

        # Method 4: marker-pdf
        try:
            markdown_output = process_with_marker_pdf(pdf_path)
            save_markdown(markdown_output, pdf_path, output_folder, "marker-pdf2")
        except Exception as e:
            print(f"Error processing {pdf_path} with marker-pdf: {e}")

        # # Method 5: markdrop
        # try:
        #     markdown_output = process_with_markdrop(pdf_path)
        #     save_markdown(markdown_output, pdf_path, output_folder, "markdrop")
        # except Exception as e:
        #     print(f"Error processing {pdf_path} with markdrop: {e}")

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

def process_with_pdfplumber(pdf_path):
    """Extracts text from a PDF using pdfplumber and formats it as Markdown."""
    markdown_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            markdown_lines.append(f"## Page {page_num}\n{text}")
    return "\n\n".join(markdown_lines)

def process_with_markdownify(pdf_path):
    """Extracts text from a PDF using PyMuPDF and converts it to Markdown with markdownify."""
    doc = fitz.open(pdf_path)
    markdown_output = ""
    for page in doc:
        html_text = page.get_text("html")  # Extract as HTML
        markdown_output += md(html_text)
    return markdown_output

def process_with_marker_pdf(pdf_path):
    config = {
        # "force_ocr": True,
        # "use_llm": True,
    }
    
    config_parser = ConfigParser(config)
    
    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
    )
    rendered = converter(pdf_path)
    text, _, images = text_from_rendered(rendered)
    return text

def process_with_markdrop(pdf_path):
    """Extracts text from a PDF using markdrop and converts it to Markdown."""
    markdrop = MarkDrop(pdf_path)
    return markdrop.to_markdown()

def save_markdown(markdown_content, pdf_path, output_folder, method_suffix):
    """Saves the Markdown content to a file with a method-specific suffix."""
    output_md_path = os.path.join(
        output_folder, f"{os.path.basename(pdf_path)}_{method_suffix}.md"
    )
    with open(output_md_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)
    # print(f"Saved Markdown ({method_suffix}) for {pdf_path} to {output_md_path}")

# Example usage
input_folder = "../data/meetings/downloaded"
output_folder = "../data/meetings/processed"
process_meetings(input_folder, output_folder)