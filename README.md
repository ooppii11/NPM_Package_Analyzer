## Overview

This project provides a set of tools to download and compare README files of npm packages. The primary goal is to fetch the README files for different versions of a package and compare them to identify any breaking changes.

## Features

1. **Download README from GitHub**: Fetches the README file from a given GitHub repository.
2. **Download README from npm**: Downloads the README file from the npm package registry.
3. **Compare README files**: Compares two README files to identify breaking changes using OpenAI and Google's Generative AI models.
4. **Fetch Multiple Versions**: Retrieves and downloads README files for the latest versions of a given npm package.
5. **Compare Multiple Versions**: Compares README files across multiple versions of an npm package.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ooppii11/npm_readme_analyzer.git
    cd npm_readme_analyzer
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Fetch and Compare README Files

1. **Set up API Keys**:

   Make sure to set the environment variables for OpenAI and Google API keys:

    ```bash
    export OPENAI_API_KEY='your-openai-api-key'
    export GOOGLE_API_KEY='your-google-api-key'
    ```

2. **Run the main script**:

    ```bash
    python npm_readme_analyzer.py
    ```

   The `main()` function in `main.py` is an example that fetches README files for the `express` package and compares the latest versions.

### Functions

- `get_readme_file_github(repo, version, readme_file_name)`: Fetches the README file from GitHub.
- `run_on_posebile_readme_file_github(repo, version)`: Tries to fetch possible README file names from GitHub.
- `get_readme_file_npm(tarball_url)`: Downloads and extracts the README file from an npm package tarball.
- `extract_data_from_package_json(package_name, version)`: Extracts package information from npm registry.
- `get_readme_file(package_name, version)`: Gets the README file for a specific package and version.
- `download_readme_file(package_name, version)`: Downloads the README file and saves it locally.
- `get_last_versions(package_name, num_of_versions)`: Retrieves the latest versions of a package from npm.
- `already_downloaded(package_name, version)`: Checks if a README file has already been downloaded.
- `feach_readme_files(package_name, num_of_versions)`: Fetches README files for the latest versions of a package.
- `compere_readme_breaking_changes_openai(readme1, readme2)`: Compares two README files using OpenAI.
- `compere_readme_breaking_changes_google(readme1, readme2)`: Compares two README files using Google's Generative AI.
- `compere_readme_files(package_name, version1, version2)`: Compares README files for two versions of a package.
- `compere_readme_versions(package_name, num_of_versions)`: Compares README files for multiple versions of a package.

## Future Enhancements

- **Documentation**: Add comprehensive documentation for each function and class.
- **Web Application**: Develop a simple web application using Flask to provide a UI for fetching and comparing README files.
