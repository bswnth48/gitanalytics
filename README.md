# AI-GitAnalytics-CLI

[![PyPI version](https://badge.fury.io/py/ai-gitanalytics-cli.svg)](https://badge.fury.io/py/ai-gitanalytics-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-GitAnalytics-CLI** is a powerful, AI-driven command-line tool that transforms your Git repository history into insightful, easy-to-read reports. It intelligently summarizes commits, groups them by theme, and provides actionable insights on code health and security.

---

## Installation

You can install the tool directly from PyPI:

```bash
pip install ai-gitanalytics-cli
```

## Configuration: Your API Key

To perform its analysis, the tool requires a free API key from **[OpenRouter](https://openrouter.ai/)**.

#### 1. Get your Free OpenRouter Key
- Sign up for a free account on [OpenRouter.ai](https://openrouter.ai/).
- Navigate to your **Account Settings** and create a new API key.
- Copy the key.

#### 2. Set up your `.env` file
The tool loads the API key from a `.env` file. You need to create this file and place it in your user **home directory**.

- **macOS/Linux:** `~/.env`
- **Windows:** `C:\Users\YourUsername\.env`

Create this file and add your key to it like this:

```
# ~/.env file
OPENROUTER_API_KEY="your-secret-key-goes-here"
```

The tool will now automatically find and use your key.

## How it Works

This tool is designed to be language-aware. It automatically detects the primary language of your repository (e.g., Python, JavaScript) and uses the appropriate tools for the job.

- **Language-Agnostic Analysis:** Thematic summaries, contributor analysis, and historical trends work for any language.
- **Language-Specific Analysis:**
    - For **Python**, it uses `bandit` for security analysis and `radon` for code complexity.
    - For **JavaScript/TypeScript**, it uses `npm audit` for security analysis.
    - *Support for more languages is coming soon!*

## Usage

Navigate to any Git repository on your machine and run the `analyze` command.

```bash
ai-gitanalytics-cli analyze .
```

This single command will perform all analyses (thematic, contributor, code health, security, and historical) and generate a detailed Markdown report in your current directory.

### Common Options

- **Generate a JSON report:**
  ```bash
  ai-gitanalytics-cli analyze . --output json
  ```

- **Analyze a specific branch:**
  ```bash
  ai-gitanalytics-cli analyze . --branch feature/new-login
  ```

- **Disable a specific analysis (e.g., security):**
  ```bash
  ai-gitanalytics-cli analyze . --no-security
  ```

- **Force a fresh analysis by ignoring the cache:**
  ```bash
  ai-gitanalytics-cli analyze . --no-cache
  ```

## Features

- **🤖 AI-Powered Summaries:** Uses advanced AI models to generate detailed, code-aware summaries for each commit.
- **🧩 Thematic Analysis:** Automatically categorizes commits into themes like `Features`, `Bug Fixes`, `Documentation`, and `Refactoring`.
- **📄 Executive Summaries:** Generates a high-level summary of the entire analysis period.
- **🛡️ Security Analysis:** Scans your code for potential vulnerabilities using industry-standard tools (`bandit` for Python, `npm audit` for JS).
-   **🩺 Code Health Insights:** Identifies high-churn files and analyzes their complexity to flag potential technical debt.
- **📊 Contributor Analysis:** Summarizes work by author to see who is contributing what.
- **📈 Historical Trends:** Tracks how your project evolves over time.
- **⚡️ Smart Caching:** Caches results to provide near-instantaneous reports on subsequent runs.

## Development

To set up a development environment with all testing dependencies, run:

```bash
uv pip install -e ".[dev]"
```

To run the automated test suite:

```bash
pytest
```