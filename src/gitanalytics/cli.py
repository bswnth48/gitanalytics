import click
from rich.console import Console
from .git_analyzer import GitAnalyzer
from .ai_summarizer import AISummarizer
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
    console.print(f"   - [bold]Start Date:[/] {start_date or 'Not specified'}")
    console.print(f"   - [bold]End Date:[/] {end_date or 'Not specified'}")
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

        console.print("\n[bold green]📊 AI-Generated Summaries:[/bold green]")
        for i, summary in enumerate(summaries):
            console.print(f"  [cyan]{i+1}.[/] {summary}")

        # --- Placeholder for future logic ---
        console.print("\n[yellow]🚧 Report generation logic not yet implemented.[/yellow]\n")

        console.print("[bold green]✅ Analysis finished.[/]")

    except git.InvalidGitRepositoryError:
        console.print(f"\n[bold red]Error:[/] The path '{repo_path}' is not a valid Git repository.")
    except ValueError as e:
        console.print(f"\n[bold red]Configuration Error:[/] {e}")
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred:[/] {e}")


if __name__ == '__main__':
    main()
