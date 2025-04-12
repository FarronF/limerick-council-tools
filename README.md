# Limerick Council Tools

This repository contains tools and utilities designed to assist with tasks related to Limerick Council operations.

## Features

- **Agenda & Minutes PDF Downloads**: Scripts for downloading minutes and agendas from all public meetings in a range of dates.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/limerick-council-tools.git
    ```
2. Navigate to the project directory:
    ```bash
    cd limerick-council-tools
    ```

## Prepare Development Environment

1. Install Python 3:
    ```bash
    sudo apt-get install python3
    ```

2. Install `python3-venv`:
    ```bash
    sudo apt-get install python3-venv
    ```

## Create and Activate Virtual Environment

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

## Usage
### Downloading agendas and minutes

To download meeting files, run the `get_meetings_files.py` script with the following arguments:

```bash
python3 get_meetings_files.py
```

PDFs will be downloaded to meetings/ folder with a structure of {year}/{month}/{day}-{meeting-name}/

All files with Agenda or Minutes in their name will be downloaded by default.

A meeting_details.json will also be generated with some basic details for reference.

### Command-Line Arguments

The script `get_meetings_files.py` supports the following command-line arguments to greater refine or extend the files downloaded:

- `--start-year` (int, default: 2014): The starting year for downloading meeting files (e.g., `2023`).
- `--start-month` (int, default: 1): The starting month (1-12).
- `--end-year` (int, default: current year): The ending year for downloading meeting files (e.g., `2024`).
- `--end-month` (int, default: current month): The ending month (1-12).
- `--meeting-filter` (list of str, optional): Filter meetings by names (case insensitive, e.g., `council budget`).
- `--file-filter` (list of str, default: `["agenda", "minutes"]`): Filter files by names (case insensitive, e.g., `agenda minutes`). Use `--file-filter None` to disable filtering.

Example usage:

```bash
python3 get_meetings_files.py --start-year 2020 --start-month 6 --end-year 2023 --end-month 12 --meeting-filter "council" "budget" --file-filter "agenda"
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