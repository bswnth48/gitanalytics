import click
import sys
from rich.console import Console
from collections import defaultdict
from .git_analyzer import GitAnalyzer
from .ai_summarizer import AISummarizer
from .report_builder import ReportBuilder
from .cache_manager import CacheManager
from .cost_monitor import CostMonitor
from .complexity_analyzer import ComplexityAnalyzer
import git

# Initialize a Rich Console for beautiful output
console = Console()

def run_analysis(repo_path, branch, start_date, end_date, output, no_cache, by_author, code_health):
    """Core logic for the analysis, separated for clarity and testability."""
    console.print(f"[bold green]🚀 Starting analysis for repository:[/] [cyan]{repo_path}[/]")
    if branch:
        console.print(f"   - [bold]Branch:[/] {branch}")
    console.print(f"   - [bold]Date Range:[/] {start_date or 'First Commit'} to {end_date or 'Latest Commit'}")
    console.print(f"   - [bold]Output Format:[/] {output}")

    cache_manager = CacheManager(repo_path)
    cost_monitor = CostMonitor()
    if no_cache:
        cache_manager.clear()
        console.print("\n[yellow]Cache has been cleared for this run.[/yellow]")

    analyzer = GitAnalyzer(repo_path)

    # --- Code Health Analysis ---
    code_health_summary = None
    if code_health:
        console.print("\n[bold yellow]🩺 Analyzing code health...[/bold yellow]")
        churn_data = analyzer.calculate_churn(branch, start_date, end_date)

        # Get top 5 most changed files
        top_churn_files = sorted(churn_data.items(), key=lambda item: item[1], reverse=True)[:5]

        if top_churn_files:
            complexity_analyzer = ComplexityAnalyzer()
            file_paths_to_analyze = [item[0] for item in top_churn_files]
            complexity_data = complexity_analyzer.analyze_files(repo_path, file_paths_to_analyze)

            # Combine churn and complexity data
            code_health_summary = []
            for file_path, churn_count in top_churn_files:
                code_health_summary.append({
                    "file_path": file_path,
                    "churn_count": churn_count,
                    "complexity": complexity_data.get(file_path, 0)
                })
            console.print("   - [green]Code health analysis complete.[/]")
        else:
            console.print("   - [yellow]No Python file changes found to analyze for code health.[/]")

    commits = analyzer.get_commits(branch, start_date, end_date)

    if not commits:
        console.print("\n[yellow]No commits found for the specified criteria.[/yellow]")
        sys.exit(0)

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

    sorted_categorized_commits = dict(sorted(categorized_commits.items()))
    console.print("   - [green]Categorization complete.[/]")

    all_summaries = [result['summary'] for result in analysis_results]
    executive_summary = summarizer.generate_executive_summary(all_summaries)

    author_summary = None
    if by_author:
        console.print("\n[bold yellow]📊 Generating contributor summary...[/bold yellow]")
        author_summary = defaultdict(lambda: defaultdict(int))
        for result in analysis_results:
            author = result['commit']['author_name']
            category = result['category']
            author_summary[author][category] += 1
        console.print("   - [green]Contributor summary complete.[/]")

    builder = ReportBuilder(repo_path, start_date, end_date)
    if output == 'markdown':
        report_file = builder.generate_markdown_report(
            sorted_categorized_commits, executive_summary, author_summary, code_health_summary
        )
    else:
        report_file = builder.generate_json_report(
            sorted_categorized_commits, executive_summary, author_summary, code_health_summary
        )

    console.print(f"\n[bold green]✅ Report successfully generated![/bold green]")
    console.print(f"   - [bold]File:[/] {report_file}")

    cost_monitor.display_summary()

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
@click.option('--by-author', is_flag=True, help='Include a contributor summary section in the report.')
@click.option('--code-health', is_flag=True, help='Include a code health (churn & complexity) section.')
def analyze(repo_path, branch, start_date, end_date, output, no_cache, by_author, code_health):
    """
    Analyze a Git repository and generate a report.
    """
    try:
        run_analysis(repo_path, branch, start_date, end_date, output, no_cache, by_author, code_health)
    except git.InvalidGitRepositoryError:
        console.print(f"\n[bold red]Error:[/] The path '{repo_path}' is not a valid Git repository.")
        sys.exit(1)
    except git.exc.GitCommandError as e:
        console.print(f"\n[bold red]Git Error:[/] Could not find branch '{branch}'. Please ensure it exists.")
        console.print(f"   - [dim]{e}[/dim]")
        sys.exit(1)
    except ValueError as e:
        console.print(f"\n[bold red]Configuration Error:[/] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred:[/] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
