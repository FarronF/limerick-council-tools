import re
from markdownify import markdownify as markdownify
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
from src.process.pdf_processors.pdf_processor_base import PdfProcessorBase 

# TODO: Split text processing, OCR processing, and Markdown conversion into separate classes
class FitzProcessor(PdfProcessorBase):
    def __init__(self, ocr_log_file_path: str):
        """
        Initialize the FitzProcessor with an OCR log file path.

        Args:
            ocr_log_file_path (str): The path to the OCR log file.
        """
        super().__init__(ocr_log_file_path)

    def process(self, pdf_path: str):
        """Extracts text from a PDF using PyMuPDF and converts it to Markdown with markdownify.
        Includes OCR for scanned PDFs."""
        doc = fitz.open(pdf_path)
        markdown_output = ""
        ocr_used = False
        print(f"XYZ Processing PDF: {pdf_path}")
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            if not page.get_text().strip():  # If no text is found, use OCR
                if not ocr_used: # Only log OCR usage once per PDF
                    self.log_ocr_usage(pdf_path)
                    ocr_used = True
                print(f"🔍 OCR used for {pdf_path} on page {page_num + 1}")
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
        return markdown_output