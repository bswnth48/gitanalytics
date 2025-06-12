# Git Analytics CLI

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered command-line tool to analyze Git repositories and generate insightful summaries of commit history.

## Overview

This tool automates the process of reviewing development activity in a Git repository. It extracts commit data within a specified date range, uses powerful AI models to understand the changes, and generates clean, easy-to-read reports in Markdown or JSON format.

## Core Features

- **AI-Powered Summaries:** Leverage large language models to get the story behind the commits.
- **Date Filtering:** Focus your analysis on specific periods (e.g., last sprint, previous quarter).
- **Flexible Output:** Generate reports in Markdown for documentation or JSON for programmatic use.
- **Cost & Performance Aware:** Built-in monitoring for API costs and processing performance.
- **Smart Caching:** Avoids re-analyzing commits that have been seen before.

## Getting Started

*(Instructions to be added once the tool is packaged and installable.)*

## Development

To set up the development environment:

1.  Ensure you have `uv` installed. If not, run:
    ```sh
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  Clone this repository.
3.  Create the virtual environment:
    ```sh
    uv venv
    ```
4.  Activate the environment:
    ```sh
    source .venv/bin/activate
    ```
5.  Install dependencies:
    ```sh
    uv pip install -r requirements.txt
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.