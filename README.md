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
- **Configurable AI:** Easily switch between different AI models supported by OpenRouter.
- **Simple Setup:** Uses a standard `.env` file for configuration.

## Getting Started

### 1. Setup

First, clone this repository and set up the development environment.

```sh
# Clone the repository
git clone <repository-url>
cd git-analytics-cli

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -e .
```

### 2. Configuration

The tool requires an API key to communicate with the AI models.

1.  Copy the example environment file:
    ```sh
    cp .env.example .env
    ```
2.  Open the new `.env` file and add your API key:
    - Get a free key from [OpenRouter](https://openrouter.ai).
    - Set `OPENROUTER_API_KEY="your-key-goes-here"`.
    - You can also change the `AI_MODEL` to any free or paid model you prefer.

### 3. Usage

Run the `analyze` command on any Git repository.

```sh
# Analyze the current directory and create a Markdown report
gitanalytics analyze

# Analyze a different repository and create a JSON report
gitanalytics analyze /path/to/your/repo --output json

# Analyze with a specific date range
gitanalytics analyze --start-date 2024-01-01 --end-date 2024-03-31
```

A report file (e.g., `git_analytics_report_YYYYMMDD_HHMMSS.md`) will be created in your current directory.

## License

This project is licensed under the MIT License.