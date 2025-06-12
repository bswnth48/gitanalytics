import click
from rich.console import Console
from collections import defaultdict
from .git_analyzer import GitAnalyzer
from .ai_summarizer import AISummarizer
from .report_builder import ReportBuilder
from .cache_manager import CacheManager
from .cost_monitor import CostMonitor
import git

# Initialize a Rich Console for beautiful output
console = Console()

@click.group()
def main():
    """
    Git Analytics CLI: Analyze Git repositories with AI.
    """
    pass

@main.command()
@click.argument('repo_path', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True), default='.')
@click.option('--branch', default=None, help='The branch to analyze. Defaults to the current active branch.')
@click.option('--start-date', help='Start date for commit analysis (YYYY-MM-DD).')
@click.option('--end-date', help='End date for commit analysis (YYYY-MM-DD).')
@click.option('--output', type=click.Choice(['markdown', 'json'], case_sensitive=False), default='markdown', help='Output format.')
@click.option('--no-cache', is_flag=True, help='Disable caching for this run.')
def analyze(repo_path, branch, start_date, end_date, output, no_cache):
    """
    Analyze a Git repository and generate a report.
    """
    console.print(f"[bold green]🚀 Starting analysis for repository:[/] [cyan]{repo_path}[/]")
    if branch:
        console.print(f"   - [bold]Branch:[/] {branch}")
    console.print(f"   - [bold]Date Range:[/] {start_date or 'First Commit'} to {end_date or 'Latest Commit'}")
    console.print(f"   - [bold]Output Format:[/] {output}")

    try:
        cache_manager = CacheManager(repo_path)
        cost_monitor = CostMonitor()
        if no_cache:
            cache_manager.clear()
            console.print("\n[yellow]Cache has been cleared for this run.[/yellow]")

        analyzer = GitAnalyzer(repo_path)
        commits = analyzer.get_commits(branch, start_date, end_date)

        if not commits:
            console.print("\n[yellow]No commits found for the specified criteria.[/yellow]")
            return

        console.print(f"\n[bold green]✅ Found {len(commits)} commits.[/bold green]")

        summarizer = AISummarizer(cache_manager, cost_monitor)
        analysis_results = summarizer.summarize_and_classify_commits(commits)

        if not analysis_results:
            console.print("\n[yellow]Could not generate analysis. This may be due to an API error or empty commits.[/yellow]")
            return

        console.print("\n[bold yellow]📊 Categorizing results...[/bold yellow]")
        categorized_commits = defaultdict(list)
        for result in analysis_results:
            categorized_commits[result['category']].append(result)

        # Sort for consistent order
        sorted_categorized_commits = dict(sorted(categorized_commits.items()))
        console.print("   - [green]Categorization complete.[/]")

        # Extract just the summaries for the executive summary
        all_summaries = [result['summary'] for result in analysis_results]
        executive_summary = summarizer.generate_executive_summary(all_summaries)

        builder = ReportBuilder(repo_path, start_date, end_date)

        if output == 'markdown':
            report_file = builder.generate_markdown_report(sorted_categorized_commits, executive_summary)
        else:
            report_file = builder.generate_json_report(sorted_categorized_commits, executive_summary)

        console.print(f"\n[bold green]✅ Report successfully generated![/bold green]")
        console.print(f"   - [bold]File:[/] {report_file}")

        # Display cost summary at the end
        cost_monitor.display_summary()

    except git.InvalidGitRepositoryError:
        console.print(f"\n[bold red]Error:[/] The path '{repo_path}' is not a valid Git repository.")
    except git.exc.GitCommandError as e:
        console.print(f"\n[bold red]Git Error:[/] Could not find branch '{branch}'. Please ensure it exists.")
        console.print(f"   - [dim]{e}[/dim]")
    except ValueError as e:
        console.print(f"\n[bold red]Configuration Error:[/] {e}")
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred:[/] {e}")


if __name__ == '__main__':
    main()
