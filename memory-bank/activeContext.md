# Active Context: Implement Thematic Analysis

## Current Focus

With code-aware summaries now complete, the next logical step is to implement **Thematic Analysis**. This will involve parsing commit messages to automatically group changes by their type (e.g., Features, Bug Fixes, Refactoring). This will add another layer of structured insight to our reports.

## Recent Changes

- Successfully implemented and tested "Code-Aware Summaries".
- The AI summarizer now analyzes both the commit message and the code diff, leading to significantly more accurate and insightful summaries.

## Next Steps

1.  **Create a Thematic Analyzer:** Implement a new function or class that can parse commit messages based on Conventional Commits prefixes (e.g., `feat:`, `fix:`, `refactor:`).
2.  **Group Commits:** The analyzer will categorize the list of commits.
3.  **Enhance Report Builder:** Update `ReportBuilder` to accept the categorized data.
4.  **Update Report Template:** Modify `report.md.j2` to dynamically render sections for each commit category (Features, Fixes, etc.).
5.  **Integrate and Test:** Update `cli.py` to orchestrate the new analysis step and verify the report now contains thematic sections.