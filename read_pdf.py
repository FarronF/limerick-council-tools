import fitz  # PyMuPDF
import os
import glob
import re
import logging
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

# List of members with their details
members = [
    {"foreName": "Dan", "surname": "McSweeney", "party": "FG", "area": "Limerick City West"},
    {"foreName": "Sarah", "surname": "Beasley", "party": "AON", "area": "Limerick City North"},
    {"foreName": "Sharon", "surname": "Benson", "party": "SF", "area": "Limerick City North"},
    {"foreName": "Daniel", "surname": "Butler", "party": "FG", "area": "Limerick City West"},
    {"foreName": "Frankie", "surname": "Daly", "party": "NP", "area": "Limerick City North"},
    {"foreName": "Maria", "surname": "Donoghue", "party": "NP", "area": "Limerick City West"},
    {"foreName": "Peter", "surname": "Doyle", "party": "FG", "area": "Limerick City East"},
    {"foreName": "Ursula", "surname": "Gavan", "party": "NP", "area": "Limerick City East"},
    {"foreName": "Seán", "surname": "Hartigan", "party": "GP", "area": "Limerick City East"},
    {"foreName": "Shane", "surname": "Hickey-O'Mara", "party": "SD", "area": "Limerick City East"},
    {"foreName": "Sarah", "surname": "Kiely", "party": "FG", "area": "Limerick City East"},
    {"foreName": "Fergus", "surname": "Kilcoyne", "party": "FF", "area": "Limerick City West"},
    {"foreName": "Joe", "surname": "Leddin", "party": "LAB", "area": "Limerick City West"},
    {"foreName": "Elisa", "surname": "O'Donovan", "party": "SD", "area": "Limerick City West"},
    {"foreName": "Kieran", "surname": "O'Hanlon", "party": "FF", "area": "Limerick City North"},
    {"foreName": "Olivia", "surname": "O'Sullivan", "party": "FG", "area": "Limerick City North"},
    {"foreName": "Joe", "surname": "Pond", "party": "FF", "area": "Limerick City East"},
    {"foreName": "Pádraigh", "surname": "Reale", "party": "LAB", "area": "Limerick City North"},
    {"foreName": "Elena", "surname": "Secas", "party": "LAB", "area": "Limerick City East"},
    {"foreName": "Catherine", "surname": "Slattery", "party": "FF", "area": "Limerick City East"},
    {"foreName": "Abul Kalam Azad", "surname": "Talukder", "party": "FF", "area": "Limerick City West"},
    
    {"foreName": "Michael", "surname": "Collins", "party": "FF", "area": "Newcastle West"},
    {"foreName": "Francis", "surname": "Foley", "party": "FF", "area": "Newcastle West"},
    {"foreName": "Liam", "surname": "Galvin", "party": "FG", "area": "Newcastle West"},
    {"foreName": "Tom", "surname": "Ruddle", "party": "FG", "area": "Newcastle West"},
    {"foreName": "Jerome", "surname": "Scanlan", "party": "NP", "area": "Newcastle West"},
    {"foreName": "John", "surname": "Sheahan", "party": "FG", "area": "Newcastle West"},
    
    {"foreName": "Bridie", "surname": "Collins", "party": "FF", "area": "Adare-Rathkeale"},
    {"foreName": "Tommy", "surname": "Hartigan", "party": "II", "area": "Adare-Rathkeale"},
    {"foreName": "Stephen", "surname": "Keary", "party": "FG", "area": "Adare-Rathkeale"},
    {"foreName": "John", "surname": "O'Donoghue", "party": "II", "area": "Adare-Rathkeale"},
    {"foreName": "Adam", "surname": "Teskey", "party": "FG", "area": "Adare-Rathkeale"},
    {"foreName": "Ger", "surname": "Ward", "party": "FF", "area": "Adare-Rathkeale"},
    
    {"foreName": "PJ", "surname": "Carey", "party": "SF", "area": "Cappamore-Kilmallock"},
    {"foreName": "Gregory", "surname": "Conway", "party": "FG", "area": "Cappamore-Kilmallock"},
    {"foreName": "Tommy", "surname": "O'Sullivan", "party": "FG", "area": "Cappamore-Kilmallock"},
    {"foreName": "Eddie", "surname": "Ryan", "party": "NP", "area": "Cappamore-Kilmallock"},
    {"foreName": "Martin", "surname": "Ryan", "party": "FF", "area": "Cappamore-Kilmallock"},
    {"foreName": "Noreen", "surname": "Stokes", "party": "FG", "area": "Cappamore-Kilmallock"},
    {"foreName": "Brigid", "surname": "Teefy", "party": "NP", "area": "Cappamore-Kilmallock"},
    
    {"foreName": "Conor", "surname": "Sheehan", "party": "LAB", "area": "Limerick City North"}
]

def get_area_from_filename(filename):
    """Returns the area based on the PDF file name."""
    filename = filename.lower()
    if "cappamore" in filename and "kilmallock" in filename:
        return "Cappamore-Kilmallock"
    elif "newcastle west" in filename:
        return "Newcastle West"
    elif "adare" in filename and "rathkeale" in filename:
        return "Adare-Rathkeale"
    elif "metropolitan" in filename in filename:
        return "Metropolitan"
    elif "limerick city and county" in filename:
        return "Full"
    return "Unknown"


def get_councillors_for_area(area):
    if area == "Full":
        return members
    elif area == "Metropolitan":
        return [m for m in members if "Limerick City" in m["area"]]
    else:
        return [m for m in members if m["area"] == area]
def remove_words_from_text(text, words):
    """Removes unwanted words and punctuation regardless of case."""
    for word in words:
        # Use regex to remove words while also handling punctuation correctly
        text = re.sub(rf"\b{re.escape(word)}\b[.,]?", "", text, flags=re.I).strip()
    return text

def remove_apologies(text):
    # Split text into lines
    lines = text.split('\n')

    # Remove lines containing the word 'apology'
    filtered_lines = [line for line in lines if 'apolog' not in line.lower()]

    # Join the filtered lines back into a single string
    filtered_text = '\n'.join(filtered_lines)
    return filtered_text

# Define regex patterns as variables
CHAIR_PATTERN = r"(?:PRESENT\s+IN\s+THE\s+CHAIR):\s*(.*?)(?=\s*(?:MEMBERS\s+PRESENT|MEMBERS\s+IN\s+ATTENDANCE))"
MEMBERS_PATTERN = r"(?:MEMBERS\s+PRESENT|MEMBERS\s+IN\s+ATTENDANCE):\s*(.*?)(?=\s*(?:OFFICIALS\s+IN\s+ATTENDANCE|$))"

def get_chair_name(text):
    """Extracts names from the 'PRESENT IN CHAIR' section only, handling extra spaces."""
    match = re.search(CHAIR_PATTERN, text, re.S)

    if match:
        extracted_text = match.group(1).strip()

        if len(extracted_text) > 500:
            logging.warning(f"Extracted chair section exceeds 500 characters! Length: {len(extracted_text)}")
            raise ValueError("Chair section is too long.")

        words_to_remove = [
            "Councillor", "Cllr", "An Cathaoirleach", "Cathaoirleach",
            "Leas-Chathaoirleach", "Príomh Chomhairleoir", ",", "."
        ]
        filtered_text = remove_words_from_text(extracted_text, words_to_remove)

        return filtered_text  # Return cleaned section

    logging.warning(text)
    return "No match found."

def get_members_section(text):
    """Extracts names from the 'MEMBERS PRESENT' or 'MEMBERS IN ATTENDANCE' section only, handling extra spaces."""
    match = re.search(MEMBERS_PATTERN, text, re.S)

    if match:
        extracted_text = match.group(1).strip()

        if len(extracted_text) > 1000:
            logging.warning(f"Extracted attendance section exceeds 1000 characters! Length: {len(extracted_text)}")
            raise ValueError("Attendance section is too long.")

        filtered_text = remove_apologies(extracted_text)
        return filtered_text  # Return extracted section

    return "No match found."


def find_duplicate_surnames(councillors):
    """Finds duplicate surnames from a list of councillor dictionaries."""
    surname_counts = Counter(c["surname"] for c in councillors)  # Extract last names
    duplicates = [surname for surname, count in surname_counts.items() if count > 1]
    
    return duplicates

def get_meeting_attendance_details(text, area):
    potential_members = get_councillors_for_area(area)
    print(potential_members)
    duplicate_surnames = find_duplicate_surnames(potential_members)
    print(duplicate_surnames)
    print("\n")
    
    chair_section = get_chair_name(text)
    members_section = get_members_section(text)
    
    isMayorPresent = False

    # Check if "Mayor Moran" is in the text and remove it
    if 'Mayor Moran' in members_section:
        isMayorPresent = True
        members_section = members_section.replace('Mayor Moran', '')  # Remove the "Mayor Moran" part
        
    members_section = members_section.replace(";", "").replace("\n", " ").replace("and", ",").replace("Councillors", "").replace("Councillor\'s", "").replace("Councillor", "").replace("MEMBERS ON-LINE", "").replace("(", "").replace(")", "").replace(".", "")
    
    # Define a regex pattern to match names (ignoring the words "Councillor" or "MEMBERS ON-LINE")
    # pattern = r'(?:Councillors|Councillor\'s|Councillor|MEMBERS ON-LINE:|,)\s*([A-Za-zÀ-ÿ’]+(?: [A-Za-zÀ-ÿ’]+)*(?: \([A-Za-z0-9\-\s]+\))?)'

    # Find all occurrences of names in the text
    # names = re.findall(pattern, members_section)
    names = members_section.split(',')
    
    # Clean up names by stripping extra whitespace
    names = [name.strip() for name in names if name.strip() != ""]
    def normalize_apostrophes(name):
        return name.replace('’', "'")

    # Normalize the names in the list
    names = [normalize_apostrophes(name) for name in names]

    removed_names = []
    # Iterate through potential_members and check for surnames in names
    for member in potential_members:
        surname = member['surname']  # Access surname from the dictionary

        # Check if the surname is in the names list
        if surname not in duplicate_surnames:
            for name in names:
                if surname in name:
                    names.remove(name)  # Remove name from the names list
                    removed_names.append(name)  # Track removed name
                    break  # Exit the loop once the name is found and removed

    # Output the list of names
    print(names)
    
    
    print(repr(chair_section))  # Separator for readability
    print("\n")
    print(repr(members_section))  # Separator for readability

    print("\n" + "=" * 80)  # Separator for readability
    


def match_members_in_section(text, members):
    """Extracts names from the 'MEMBERS PRESENT' section only."""
    pattern = r"PRESENT IN THE CHAIR:\s*(.*?)\n(?:OFFICIALS IN ATTENDANCE)"
    match = re.search(pattern, text, re.S)

    return match

def read_pdfs_from_folder(folder_path):
    """Reads all PDFs in a folder and processes them."""
    folder_path = os.path.abspath(folder_path)
    print(f"Checking for PDFs in: {folder_path}")  

    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    area_counts = {"Cappamore-Kilmallock": 0, "Newcastle West": 0, "Adare-Rathkeale": 0, "Metropolitan": 0}

    for pdf_file in pdf_files:
        print(f"\n📄 Reading: {pdf_file}\n" + "-" * 50)

        # Extract area from file name
        area = get_area_from_filename(pdf_file)
        print(f"Detected area: {area}")

        doc = fitz.open(pdf_file)
        text = "\n".join(page.get_text() for page in doc)

        get_meeting_attendance_details(text, area)
        
        
        
        # Identify surnames present in the text
        # surnames_in_text = [line.strip() for line in text.splitlines() if line.strip()]
        
        # Check each member if their surname appears in the text for the respective area
        # members_present = []
        # for member in members:
        #     if member['area'] == area and member['surname'] in surnames_in_text:
        #         members_present.append(member)

        # # Count members present for the area
        # area_counts[area] += len(members_present)

        # # Display members present
        # if members_present:
        #     print(f"\n🔹 Members Present in {area}:")
        #     for member in members_present:
        #         print(f"   - {member['foreName']} {member['surname']} ({member['party']})")
        # else:
        #     print(f"\n❌ No members present in {area}.")

        # print("\n" + "=" * 80)  # Separator for readability

    print("\nArea Member Counts: ")
    for area, count in area_counts.items():
        print(f"{area}: {count} members present.")

# Run the function with the folder
pdf_folder = "PDFs"
read_pdfs_from_folder(pdf_folder)
