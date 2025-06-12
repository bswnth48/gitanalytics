# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - YYYY-MM-DD

### Added
- **Thematic Analysis:**
  - Automatically categorizes commits into themes (e.g., Features, Bug Fixes) based on Conventional Commit prefixes.
  - Report format updated to group commits under their respective themes.
- **Code-Aware Summaries:**
  - Upgraded AI summarizer to analyze code diffs alongside commit messages, resulting in significantly more accurate and context-rich summaries.
- **Report Builder:**
  - Implemented `ReportBuilder` to generate analysis reports in Markdown and JSON.
- **AI Summarizer:**
  - Implemented `AISummarizer` to generate summaries for commits and a high-level executive summary for the entire analysis period.
- **Configuration System:**
  - Added support for a `.env` file to manage API keys and model names securely.
- **Git Analyzer:**
  - Implemented `GitAnalyzer` class to extract commits and their diffs.
- **CLI Skeleton & Project Initialization:**
  - Set up project structure, CLI, and all documentation.

## [0.1.0] - YYYY-MM-DD

### Added
- **Code-Aware Summaries:**
  - Upgraded AI summarizer to analyze code diffs alongside commit messages, resulting in significantly more accurate and context-rich summaries.
  - Enhanced `GitAnalyzer` to extract the code diff for each commit.
- **Report Builder:**
  - Implemented `ReportBuilder` to generate analysis reports.
  - Added support for both Markdown (using a Jinja2 template) and JSON output formats.
  - Reports are saved to uniquely named files in the current directory.
- **AI Summarizer:**
  - Implemented `AISummarizer` to generate summaries for commits via OpenRouter.
  - Added a high-level executive summary for the entire analysis period.
- **Configuration System:**
  - Added support for a `.env` file to manage API keys and model names securely.
- **Git Analyzer:**
  - Implemented `GitAnalyzer` class to extract commits using `GitPython`.
- **CLI Skeleton:**
  - Implemented the main command group and `analyze` command in `src/gitanalytics/cli.py`.
- **Project Initialization:**
  - Set up project structure with `uv` package manager and all documentation.