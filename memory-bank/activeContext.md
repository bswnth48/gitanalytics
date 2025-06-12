# Active Context: Advanced Analytics - Code Churn & Complexity

## Current Focus

Having added Contributor Analysis, we are now moving to the second advanced analytics feature: **Code Churn & Complexity**. The goal is to analyze the repository to identify "hotspots"—files that are frequently changed—and to measure their cyclomatic complexity. This will provide insights into potential technical debt and areas of the codebase that might be difficult to maintain.

## Recent Changes

- Successfully implemented and tested "Contributor Analysis", which adds an optional author-centric summary to the report.
- Added a `--by-author` flag to the CLI to control this feature.
- Updated the report templates and builder to handle and display the new contributor data.

## Next Steps

1.  **Add Dependency:** Add the `radon` library to our `pyproject.toml` file to provide complexity analysis capabilities.
2.  **Enhance Git Analyzer:** Update `GitAnalyzer` to track file modification statistics across all commits to calculate code churn.
3.  **Create Complexity Analyzer:** Build a new component that uses `radon` to analyze the complexity of given source files.
4.  **Integrate & Report:** Update the main `run_analysis` logic to combine churn and complexity data and pass it to the `ReportBuilder` for inclusion in a new "Code Health" section of the report.
5.  **Add Tests:** Write tests for the churn and complexity analysis logic.