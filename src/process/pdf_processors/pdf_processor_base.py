import os
from datetime import datetime
from abc import ABC, abstractmethod

from src.logging.file_logger import FileLoggerSingleton

class PdfProcessorBase(ABC):
    def log_ocr_usage(self, pdf_path: str):
        """
        Logs the usage of OCR for a given PDF file.

        Args:
            pdf_path (str): The path to the PDF file for which OCR was used.
        """
        
        FileLoggerSingleton._instance.log("ocr_used", f"{pdf_path}")

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