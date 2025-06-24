from typing import List, TypedDict
from src.types.file_details import FileDetails

class MeetingDetails(TypedDict):
    name: str
    href: str
    datetime: str
    files: List[FileDetails]