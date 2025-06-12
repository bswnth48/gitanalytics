import openai
from typing import List
from rich.console import Console

from .git_analyzer import Commit
from .config import settings

# Initialize a Rich Console for beautiful output
console = Console()

class AISummarizer:
    """
    Uses an AI model via OpenRouter to summarize commit messages.
    """
    def __init__(self):
        """
        Initializes the AISummarizer using settings from config.
        """
        if not settings.OPENROUTER_API_KEY or settings.OPENROUTER_API_KEY == "your-key-goes-here":
            raise ValueError("OpenRouter API key not found. Please create a .env file and set the OPENROUTER_API_KEY.")

        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
        )
        self.model = settings.AI_MODEL

    def summarize_commits(self, commits: List[Commit]) -> List[str]:
        """
        Generates summaries for a list of commit messages.

        Args:
            commits: A list of Commit objects.

        Returns:
            A list of strings, where each string is a summary of a commit.
        """
        if not commits:
            return []

        console.print(f"\n[bold yellow]🤖 Contacting AI ({self.model}) for summarization...[/bold yellow]")

        # For now, we will summarize one by one. Batching can be a future optimization.
        summaries = []
        for commit in commits:
            try:
                prompt = f"""
                Analyze the following git commit and provide a concise, one-sentence summary of its purpose.

                Author: {commit.author_name}
                Date: {commit.date.strftime('%Y-%m-%d')}
                Message:
                ---
                {commit.message}
                ---

                One-sentence summary:
                """

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer who provides concise git commit summaries."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.5,
                    max_tokens=60,
                )
                summary = response.choices[0].message.content.strip()
                summaries.append(summary)
                console.print(f"   - [green]Summarized commit[/] [cyan]{commit.commit_hash[:7]}[/]")
            except openai.APIError as e:
                error_message = f"OpenAI API error for commit {commit.commit_hash[:7]}: {e}"
                console.print(f"[bold red]Error:[/] {error_message}")
                summaries.append(f"Error summarizing commit: {commit.commit_hash[:7]}")

        return summaries
