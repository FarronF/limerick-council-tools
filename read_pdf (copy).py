import fitz  # PyMuPDF
import os
import glob
import re

def extract_members(text):
    """Extracts names from the 'MEMBERS PRESENT' section only."""
    pattern = r"MEMBERS PRESENT:\s*(.*?)\n(?:OFFICIALS IN ATTENDANCE)"
    match = re.search(pattern, text, re.S)

    if match:
        members_section = match.group(1).strip()
        # Split names using commas and new lines
        members = re.split(r",|\n", members_section)
        return [name.strip() for name in members if name.strip()]
    return []

def read_pdfs_from_folder(folder_path):
    """Reads all PDFs in a folder and extracts 'Members Present'."""
    folder_path = os.path.abspath(folder_path)
    print(f"Checking for PDFs in: {folder_path}")  

    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    for pdf_file in pdf_files:
        print(f"\n📄 Reading: {pdf_file}\n" + "-" * 50)

        doc = fitz.open(pdf_file)
        text = "\n".join(page.get_text() for page in doc)

        # Extract Members Present
        members_present = extract_members(text)

        # Print members present
        if members_present:
            print("\n🔹 Members Present:")
            for name in members_present:
                print(f"   - {name}")
        else:
            print("\n❌ No 'Members Present' section found.")

        print("\n" + "=" * 80)  # Separator for readability

# Run the function with your relative folder
pdf_folder = "PDFs"
read_pdfs_from_folder(pdf_folder)


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
    {"foreName": "Pádraigh", "surname": "Reale", "party": "LAB", "area": "Limerick City North", "startDate": "2024-12-19"},
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
    {"foreName": "Tommy", "surname": "O’Sullivan", "party": "FG", "area": "Cappamore-Kilmallock"},
    {"foreName": "Eddie", "surname": "Ryan", "party": "NP", "area": "Cappamore-Kilmallock"},
    {"foreName": "Martin", "surname": "Ryan", "party": "FF", "area": "Cappamore-Kilmallock"},
    {"foreName": "Noreen", "surname": "Stokes", "party": "FG", "area": "Cappamore-Kilmallock"},
    {"foreName": "Brigid", "surname": "Teefy", "party": "NP", "area": "Cappamore-Kilmallock"},
    
    {"foreName": "Conor", "surname": "Sheehan", "party": "LAB", "area": "Limerick City North", "endDate": "2024-12-19"}
]
