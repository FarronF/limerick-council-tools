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

### Prepare Dev Environment
* install python 3
* apt-get install python3-venv

### Create and activate Virtual Environment with dependencies
    python3 -m venv .env
    .env/Scripts/activate[.bat|ps1]

## Usage
### Downloading agendas and minutes

To download meeting files, run the `get_meetings_files.py` script with the following arguments:

```bash
python get_meetings_files.py <start_year> <start_month> <end_year> <end_month>
```

Replace `<start_year>`, `<start_month>`, `<end_year>`, and `<end_month>` with the desired date range.

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