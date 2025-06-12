# Active Context: Implement Cost Monitoring

## Current Focus

With performance and efficiency improved by caching, our new focus is on providing visibility into the operational costs of the tool. The goal is to implement a **Cost Monitor** that tracks API token usage and provides an estimated cost for each analysis run.

## Recent Changes

- Successfully implemented and tested "Smart Caching", which drastically reduces API calls and improves performance on repeated analyses.
- Added a `--no-cache` flag for control over caching behavior.
- Fixed a bug related to date formatting when loading results from the cache.

## Next Steps

1.  **Create Cost Monitor:** Implement a `CostMonitor` class in `src/gitanalytics/cost_monitor.py`. This class will hold pricing information for various AI models and track token usage.
2.  **Integrate with AI Summarizer:** Modify `AISummarizer` to track the token usage from each API call (both for summaries and the executive summary) via the `CostMonitor`.
3.  **Integrate with CLI:** Update the `analyze` command in `cli.py` to instantiate the `CostMonitor`, pass it to the summarizer, and display a cost summary at the end of the analysis.
4.  **Test:** Run an analysis with `--no-cache` to ensure API calls are made and that the cost calculation is displayed correctly.