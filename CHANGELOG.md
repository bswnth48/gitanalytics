# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - YYYY-MM-DD

### Added
- **AI Summarizer:**
  - Implemented `AISummarizer` to generate summaries for commits via OpenRouter.
  - Integrated into the CLI to display AI-generated results.
- **Configuration System:**
  - Added support for a `.env` file to manage API keys and model names securely (Thanks for the suggestion!).
  - Created `config.py` with `pydantic-settings` for robust settings management.
  - Added `.gitignore` to protect environment files.
- **Git Analyzer:**
  - Implemented `GitAnalyzer` class to extract commits using `GitPython`.
  - Added date filtering capabilities.
  - Defined a `Commit` Pydantic model for structured data.
  - Integrated the analyzer with the CLI to display the commit count.
- **CLI Skeleton:**
  - Implemented the main command group and `analyze` command in `src/gitanalytics/cli.py`