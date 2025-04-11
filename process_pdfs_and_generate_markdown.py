import os
import glob
import fitz

def process_pdfs_and_generate_markdown(input_folder, output_folder):
    """Processes PDFs, creates folder structure, and generates markdown files."""
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = glob.glob(os.path.join(input_folder, "*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    for pdf_file in pdf_files:
        file_name = os.path.basename(pdf_file)
        base_name, _ = os.path.splitext(file_name)
        markdown_folder = os.path.join(output_folder, base_name)

        if not os.path.exists(markdown_folder):
            os.makedirs(markdown_folder)

        doc = fitz.open(pdf_file)
        text = "\n".join(page.get_text() for page in doc)

        markdown_file = os.path.join(markdown_folder, f"{base_name}.md")
        with open(markdown_file, "w", encoding="utf-8") as md_file:
            md_file.write(f"# {base_name}\n\n{text}")

        print(f"Processed and created markdown for: {file_name}")

    readme_path = os.path.join(output_folder, "README.md")
    with open(readme_path, "w", encoding="utf-8") as readme_file:
        readme_file.write("# Processed PDFs\n\n")
        readme_file.write("This folder contains markdown files generated from the processed PDFs.\n")

    print("README.md created in the output folder.")

# Example usage
input_folder = "data/meetings/downloaded"
output_folder = "data/meetings/processed"
process_pdfs_and_generate_markdown(input_folder, output_folder)