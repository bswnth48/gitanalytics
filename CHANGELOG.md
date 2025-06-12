# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - YYYY-MM-DD

### Changed
- **Upgraded Thematic Analysis to AI-Powered Classification:**
  - Replaced the rule-based thematic analyzer with a more robust, single-call AI classification system.
  - Enhanced the AI prompt with detailed category descriptions to improve accuracy and summary quality.
  - The tool can now reliably categorize commits from any repository, regardless of commit message conventions.

### Added
- **Branch Selection:**
  - Added a `--branch` option to the `analyze` command to allow analysis of any branch, not just the currently active one.
  - The `GitAnalyzer` was enhanced to correctly identify commits unique to the specified branch.
- **Smart Caching:**
  - Implemented a caching system to store AI-generated summaries, dramatically improving performance for repeated analyses.
  - Added a `--no-cache` flag to bypass the cache.
- **Cost Monitoring:**
  - Integrated a cost monitor to track API token usage and provide an estimated cost for each analysis run.

### Fixed
- **Date Handling in Reports:** Corrected a bug where dates from cached results were not being formatted correctly, causing report generation to fail.

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

# Progress: Git Analytics CLI

## Current Status: Version 0.4.0 (Implementing Automated Tests)

## What Works
- **Complete Project Scaffolding**
- **Basic CLI**
- **Git Analyzer**
- **AI Summarizer**
- **AI Classifier**
- **Branch Selection**
- **Report Builder**
- **Smart Caching**
- **Cost Monitoring**

## What's Left to Build
### Production-Ready Features
- **Automated Testing (`tests/`)**: A full `pytest` suite. *(In Progress)*

## Known Issues
- None at this time.