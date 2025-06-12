from typing import List, Dict, Tuple
from collections import defaultdict
import re

from .git_analyzer import Commit

# Mapping of commit prefixes to their full titles for the report
CONVENTIONAL_COMMIT_MAP = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "docs": "Documentation",
    "style": "Styling",
    "refactor": "Code Refactoring",
    "test": "Tests",
    "chore": "Chores",
    "perf": "Performance Improvements",
    "build": "Build System",
    "ci": "Continuous Integration",
}

def analyze_themes(commits_with_summaries: List[Tuple[Commit, str]]) -> Dict[str, List[Dict]]:
    """
    Analyzes commits to group them by conventional commit type.

    Args:
        commits_with_summaries: A list of tuples, each containing a Commit object
                                 and its corresponding AI summary.

    Returns:
        A dictionary where keys are theme titles (e.g., "Features") and
        values are lists of commit/summary dictionaries.
    """
    categorized_commits = defaultdict(list)

    for commit, summary in commits_with_summaries:
        commit_message = commit.message.lower()

        # Use regex to find a prefix like "feat:" or "fix(scope):"
        match = re.match(r"^(\w+)(?:\(.*\))?:", commit_message)

        if match:
            commit_type = match.group(1)
            category_title = CONVENTIONAL_COMMIT_MAP.get(commit_type, "Miscellaneous")
        else:
            category_title = "Miscellaneous"

        categorized_commits[category_title].append({
            'commit': commit,
            'summary': summary
        })

    # Sort the dictionary by key for a consistent report order
    return dict(sorted(categorized_commits.items()))