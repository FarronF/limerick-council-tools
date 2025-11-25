from typing import List, TypedDict
from src.pdf_parser.types.file_details import FileDetails

class MeetingDetails(TypedDict):
    name: str
    href: str
    datetime: str
    files: List[FileDetails]