## Overview

The NPM Package Analyzer is a Python-based tool designed to compare README files of different versions of NPM packages. It aims to identify changes, especially breaking changes, between versions by leveraging AI-based comparison methods

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

### CLI Client

The `CLI_Client.py` script provides a command-line interface to interact with the npm package README analyzer. This script allows users to fetch and compare README files for different versions of an npm package interactively.

#### Usage

1. **Set up API Keys**:
   Ensure that your environment variables for the required API keys are set, or be prepared to enter them when prompted.

2. **Run the CLI Client**:
   Execute the script using Python:

   ```bash
   python CLI_Client.py
   ```

3. **Provide Input**:
   - **Package Name**: Enter the name of the npm package you want to analyze.
   - **Number of Versions**: Enter the number of recent versions you want to compare.
   - **Comparison Method**: Choose a method for comparing the README files from the options provided.

   If the chosen comparison method requires an API key and it's not already set in the environment variables, you'll be prompted to enter it.

#### Example

Here's an example interaction with the CLI client:

```bash
example will be added
```

## Future Enhancements

- **Web Application**: Develop a simple web application using Flask to provide a UI for fetching and comparing README files.

---
