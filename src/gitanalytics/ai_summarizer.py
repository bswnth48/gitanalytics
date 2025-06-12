import openai
import json
from typing import List, Dict
from rich.console import Console

from .git_analyzer import Commit
from .config import settings

# Initialize a Rich Console for beautiful output
console = Console()

# Define categories with descriptions to guide the AI
CATEGORIES_WITH_DESC = {
    "Features": "New user-facing features or major enhancements.",
    "Bug Fixes": "Fixing a bug, crash, or an issue in the code.",
    "Documentation": "Changes to README, guides, or code comments.",
    "Code Refactoring": "Improving code structure without changing its external behavior.",
    "Tests": "Adding or improving automated tests.",
    "Build System": "Changes to build scripts, CI/CD, or dependencies.",
    "Performance Improvements": "Code changes that specifically improve performance.",
    "Chores": "Routine tasks, maintenance, setup, or other non-functional changes."
}
CATEGORIES = list(CATEGORIES_WITH_DESC.keys())

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

    def summarize_and_classify_commits(self, commits: List[Commit]) -> List[Dict]:
        """
        Generates a detailed summary and an accurate classification for each commit.
        """
        if not commits:
            return []

        console.print(f"\n[bold yellow]🤖 Generating summaries and classifications...[/bold yellow]")

        results = []
        for commit in commits:
            try:
                max_diff_length = 4000
                truncated_diff = commit.diff[:max_diff_length]

                prompt = f"""
                Analyze the git commit message and code diff below.

                **Your Tasks:**
                1.  **Summarize:** Write a detailed, one-sentence summary. The summary MUST explain the change's purpose and impact, focusing on WHAT was changed and WHY.
                2.  **Classify:** Choose ONE category for the commit from the list provided.

                **Category Definitions:**
                {json.dumps(CATEGORIES_WITH_DESC, indent=2)}

                **Output Format:**
                You MUST respond with a single, valid JSON object with two keys: "summary" (string) and "category" (string).

                **Commit Data:**

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
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer who provides detailed, code-aware summaries and accurate classifications of git commits. You must respond with a valid JSON object."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.1, # Reduced for more deterministic output
                    max_tokens=250,  # Increased for potentially longer summaries
                )

                response_data = json.loads(response.choices[0].message.content)
                summary = response_data.get("summary", "No summary provided.")
                category = response_data.get("category", "Chores")

                # Ensure the AI returns a valid category
                if category not in CATEGORIES:
                    category = "Chores" # Default to Chores if AI hallucinates a category

                results.append({'commit': commit, 'summary': summary, 'category': category})

            except (openai.APIError, json.JSONDecodeError) as e:
                console.print(f"[bold red]Error processing commit {commit.commit_hash[:7]}:[/] {e}")
                results.append({'commit': commit, 'summary': 'Error processing commit.', 'category': 'Chores'})

        console.print(f"   - [green]Processed {len(results)} commits.[/]")
        return results

    def generate_executive_summary(self, commit_summaries: List[str]) -> str:
        """
        Generates a high-level executive summary from a list of commit summaries.
        """
        console.print(f"\n[bold yellow]✨ Generating high-level executive summary...[/bold yellow]")

        summaries_text = "\n".join(f"- {s}" for s in commit_summaries)
        prompt = f"""
        Based on the following list of commit summaries, please provide a high-level,
        three-sentence executive summary.

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
                    {"role": "system", "content": "You are a CTO who provides high-level summaries of development progress."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.6,
                max_tokens=200,
            )
            executive_summary = response.choices[0].message.content.strip()
            console.print("   - [green]Executive summary created.[/]")
            return executive_summary
        except openai.APIError as e:
            console.print(f"[bold red]Error during executive summary generation:[/] {e}")
            return "Could not generate executive summary due to an API error."
