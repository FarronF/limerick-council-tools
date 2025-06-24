import os
from datetime import datetime
from abc import ABC, abstractmethod

class PdfProcessorBase(ABC):
    def __init__(self, ocr_log_file_path: str):
        """
        Initialize the PdfProcessorBase with an OCR log file path.

        Args:
            ocr_log_file_path (str): The path to the OCR log file.
        """
        self.ocr_log_file_path = ocr_log_file_path

    # TODO: logging is far too complicated, look at alternatives. Own class?
    def log_ocr_usage(self, pdf_path: str):
        """
        Logs the usage of OCR for a given PDF file.

        Args:
            pdf_path (str): The path to the PDF file for which OCR was used.
        """
        
        # Ensure the directory for the log file exists
        os.makedirs(os.path.dirname(self.ocr_log_file_path), exist_ok=True)
        
        # Append the PDF path to the log file
        with open(self.ocr_log_file_path, "a") as log_file:
            log_file.write(f"{pdf_path}\n")

    @abstractmethod
    def process(self, pdf_path: str):
        """
        Process the given PDF file.

        Args:
            pdf_path (str): The path to the PDF file to process.

        Returns:
            None
        """
        pass