# Active Context: Implement Branch Selection

## Current Focus

Having successfully implemented a robust, AI-powered classification system, our next goal is to add **Branch Selection**. This will enhance the tool's flexibility by allowing users to analyze any branch in the repository, not just the currently checked-out one.

## Recent Changes

- Successfully implemented and tested "AI-Powered Classification".
- Refined the AI prompt to include detailed category descriptions, resulting in more accurate classifications and more detailed summaries.
- The tool can now intelligently categorize commits in any repository, regardless of whether it uses Conventional Commit standards.
- Deprecated the old rule-based `thematic_analyzer.py`.

## Next Steps

1.  **Enhance CLI:** Add a `--branch` option to the `analyze` command in `cli.py`.
2.  **Enhance Git Analyzer:** Modify the `get_commits` method in `git_analyzer.py` to accept the new `branch` parameter and use it to iterate over the correct commits.
3.  **Test:** Run the analysis on a specific branch to verify the new functionality works as expected.
4.  **Update Documentation:** Update the `README.md` with instructions for the new `--branch` option.