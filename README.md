# Limerick Council Tools

This repository contains tools and utilities designed to assist with tasks related to Limerick Council operations.

This is used to generate the meeting files in [Limerick Council Meetings](https://github.com/FarronF/limerick-council-meetings)

## Features

- **Meeting PDF Downloads and Parsing**: Script for downloading PDFs from all public meetings in a range of dates and parsing the contents to export to markdown.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/farronf/limerick-council-tools.git
    ```
2. Navigate to the project directory:
    ```bash
    cd limerick-council-tools
    ```
## Quick Start With Docker
Install Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop).

Once installed:

Build the docker image
```bash
docker build -t limerick-council-tools .
```

Run the image in a docker container. The following command will run in interactive mode with the shell inside the container. If you wish to access the downloaded/processed files outside of the Docker container make sure to update the /your/local/data section with a valid destination.
```bash
docker run -it --rm -v /your/local/data:/app/data limerick-council-tools sh
```

If access outside the container is not needed it can be run without the volume. All data will be lost when the container is stopped in this case.
```bash
docker run -it --rm limerick-council-tools sh
```

When finished to exit docker enter: 
```bash
exit
```

## Usage
Once docker is running in interactive mode

To download and process all meetings agenda and minutes files call
```bash
python3 main.py
```

PDFs will be downloaded to data/meetings/downloaded folder with a structure of {year}/{month}/{day}-{meeting-name}/

All files with Agenda or Minutes in their name will be downloaded by default.

A meeting_details.json will also be generated with some basic details for reference.

Meetings will then be processed.

PDFs for these meetings will be parsed to extract the text and converted to markdown. Files containing the extracted text as markdown along with a README.md summary of the meeting details will be saved to limerick-counil-meetings/meetings folder with the same sub folder structure.

### Command-Line Arguments

The script `main.py` supports the following command-line arguments to greater refine or extend the files downloaded:

- `--start-year` (int, default: 2014): The starting year (e.g., `2023`).
- `--start-month` (int, default: 1): The starting month for the starting year, future years will start from January (1-12).
- `--end-year` (int, default: current year): The ending year (e.g., `2024`).
- `--end-month` (int, default: current month): The ending month for the ending year, previous years will end on December (1-12).
- `--meeting-filter` (list of str, optional): Filter meetings by names, this will include any meetings with . When None all meetings will be included. (case insensitive, e.g., ["council budget"]).
- `--file-filter` (list of str, default: `["agenda", "minutes"]`): Filter files by names (case insensitive, e.g., `agenda minutes`). Use `--file-filter None` to disable filtering.
- `--download-location` (str, default: `./data/downloaded`): Location to save downloaded files.
- `--output-location` (str, default: `./data/meetings`): Location to output processed markdown files.
- `--logs-location` (str, default: `./.logs`): Location to output logs.
- `--dont-download` (flag): Do not download new files, process existing files only.
- `--dont-process` (flag): Do not process files to markdown, only download.
- `--delete-downloads-after-complete` (flag): Delete downloaded files after processing. Note: This will delete all files in download-location not just files that were downloaded

Example usage:

```bash
python3 main.py --start-year 2020 --start-month 6 --end-year 2023 --end-month 12 --meeting-filter ["council budget"] --file-filter "agenda" --delete-downloads-after-complete
```

## Alternative Setup for local development
If you are making changes to code this might be preferable to Docker.

### Prepare Development Environment

1. Install Python 3:

    - On Linux:
        ```bash
        sudo apt-get install python3
        ```
    - On Windows:  
      Download and install Python from [python.org](https://www.python.org/downloads/).  
      Make sure to check "Add Python to PATH" during installation.

2. Install `python3-venv`:

    - On Linux:
        ```bash
        sudo apt-get install python3-venv
        ```
    - On Windows:  
      The `venv` module is included by default with Python 3.3 and above. No extra installation is needed.

### Create and Activate Virtual Environment

1. Create a virtual environment:
    ```bash
    python3 -m venv .env
    ```

2. Activate the virtual environment:
    - On Linux/MacOS:
        ```bash
        source .env/bin/activate
        ```
    - On Windows:
        ```bash
        .env\Scripts\activate
        ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to your branch:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or suggestions, please message [farronf](https://github.com/farronf) on GitHub.