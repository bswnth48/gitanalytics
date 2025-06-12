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
        if not settings.OPENROUTER_API_KEY or "your-key-goes-here" in settings.OPENROUTER_API_KEY:
            raise ValueError("OpenRouter API key not found. Please create a .env file and set the OPENROUTER_API_KEY.")

        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
        )
        self.model = settings.AI_MODEL

    def summarize_commits(self, commits: List[Commit]) -> List[str]:
        """
        Generates summaries for a list of commit messages and their diffs.
        """
        if not commits:
            return []

        console.print(f"\n[bold yellow]🤖 Generating code-aware summaries...[/bold yellow]")

        summaries = []
        for commit in commits:
            try:
                # Truncate diff to manage token count
                max_diff_length = 4000
                truncated_diff = commit.diff[:max_diff_length]

                prompt = f"""
                As an expert software engineer, analyze the following git commit message and the accompanying code diff.
                Provide a concise, one-sentence summary that explains the change's purpose and impact.
                Focus on WHAT was changed and WHY, integrating insights from both the message and the code.

                Commit Message:
                ---
                {commit.message}
                ---

                Code Diff:
                ---
                {truncated_diff}
                ---
                """
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer who provides concise, code-aware summaries of git commits."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.4,
                    max_tokens=80, # Increased slightly for more detailed summaries
                )
                summary = response.choices[0].message.content.strip()
                summaries.append(summary)
            except openai.APIError as e:
                error_message = f"API error for commit {commit.commit_hash[:7]}: {e}"
                console.print(f"[bold red]Error:[/] {error_message}")
                summaries.append(f"Error summarizing commit.")

        console.print(f"   - [green]Summarized {len(summaries)} commits.[/]")
        return summaries

    def generate_executive_summary(self, commit_summaries: List[str]) -> str:
        """
        Generates a high-level executive summary from a list of commit summaries.
        """
        console.print(f"\n[bold yellow]✨ Generating high-level executive summary...[/bold yellow]")

        summaries_text = "\n".join(f"- {s}" for s in commit_summaries)
        prompt = f"""
        Based on the following list of commit summaries from a development period, please provide a high-level,
        three-sentence executive summary. This summary should capture the main themes of the work, such as new features,
        major refactors, or significant bug fixes.

        Commit Summaries:
        ---
        {summaries_text}
        ---

        Executive Summary (3 sentences):
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a CTO who provides high-level summaries of development progress for technical and non-technical stakeholders."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.6,
                max_tokens=200,
            )
            executive_summary = response.choices[0].message.content.strip()
            console.print("   - [green]Executive summary created.[/]")
            return executive_summary
        except openai.APIError as e:
            error_message = f"API error during executive summary generation: {e}"
            console.print(f"[bold red]Error:[/] {error_message}")
            return "Could not generate executive summary due to an API error."
