import click
from rich.console import Console
from .git_analyzer import GitAnalyzer
from .ai_summarizer import AISummarizer
from .report_builder import ReportBuilder
from .thematic_analyzer import analyze_themes
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
@click.option('--start-date', help='Start date for commit analysis (YYYY-MM-DD).')
@click.option('--end-date', help='End date for commit analysis (YYYY-MM-DD).')
@click.option('--output', type=click.Choice(['markdown', 'json'], case_sensitive=False), default='markdown', help='Output format.')
def analyze(repo_path, start_date, end_date, output):
    """
    Analyze a Git repository and generate a report.
    """
    console.print(f"[bold green]🚀 Starting analysis for repository:[/] [cyan]{repo_path}[/]")
    console.print(f"   - [bold]Date Range:[/] {start_date or 'First Commit'} to {end_date or 'Latest Commit'}")
    console.print(f"   - [bold]Output Format:[/] {output}")

    try:
        analyzer = GitAnalyzer(repo_path)
        commits = analyzer.get_commits(start_date, end_date)

        if not commits:
            console.print("\n[yellow]No commits found in the specified date range.[/yellow]")
            return

        console.print(f"\n[bold green]✅ Found {len(commits)} commits.[/bold green]")

        summarizer = AISummarizer()
        summaries = summarizer.summarize_commits(commits)

        console.print("\n[bold yellow]📊 Analyzing themes...[/bold yellow]")
        commits_with_summaries = list(zip(commits, summaries))
        categorized_commits = analyze_themes(commits_with_summaries)
        console.print("   - [green]Thematic analysis complete.[/]")

        executive_summary = summarizer.generate_executive_summary(summaries)

        builder = ReportBuilder(repo_path, start_date, end_date)

        if output == 'markdown':
            report_file = builder.generate_markdown_report(categorized_commits, executive_summary)
        else: # output == 'json'
            report_file = builder.generate_json_report(categorized_commits, executive_summary)

        console.print(f"\n[bold green]✅ Report successfully generated![/bold green]")
        console.print(f"   - [bold]File:[/] {report_file}")

    except git.InvalidGitRepositoryError:
        console.print(f"\n[bold red]Error:[/] The path '{repo_path}' is not a valid Git repository.")
    except ValueError as e:
        console.print(f"\n[bold red]Configuration Error:[/] {e}")
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred:[/] {e}")


if __name__ == '__main__':
    main()
