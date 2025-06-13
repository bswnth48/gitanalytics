import git
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from collections import defaultdict

class Commit(BaseModel):
    """
    Pydantic model to represent a single Git commit.
    """
    commit_hash: str = Field(..., alias='hexsha')
    author_name: str
    author_email: str
    date: datetime
    message: str
    diff: str

    class Config:
        arbitrary_types_allowed = True

class GitAnalyzer:
    """
    Analyzes a Git repository to extract commit information and calculate churn.
    """
    def __init__(self, repo_path: str):
        """
        Initializes the GitAnalyzer.

        Args:
            repo_path: The file path to the Git repository.

        Raises:
            git.InvalidGitRepositoryError: If the path is not a valid Git repository.
            git.NoSuchPathError: If the path does not exist.
        """
        try:
            self.repo = git.Repo(repo_path, search_parent_directories=True)
        except (git.InvalidGitRepositoryError, git.NoSuchPathError) as e:
            print(f"Error: {e}")
            raise

        # Exclude common non-source files from diffs
        self.exclude_patterns = ['*.json', '*.md', '*.txt', 'LICENSE', '.gitignore']

    def get_commits(self, branch: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Commit]:
        """
        Extracts commits. If a branch is specified, it shows commits on that
        branch which are not in the 'main' branch. Otherwise, it shows commits
        from the current HEAD.
        """
        if branch:
            commit_spec = f"main..{branch}"
        else:
            commit_spec = self.repo.head.ref

        kwargs = {}
        if start_date:
            kwargs['after'] = start_date
        if end_date:
            kwargs['before'] = end_date

        try:
            commits_iter = self.repo.iter_commits(commit_spec, **kwargs)
        except git.GitCommandError:
            commits_iter = self.repo.iter_commits(branch or self.repo.head.ref, **kwargs)

        commit_list = []
        for commit in commits_iter:
            try:
                if commit.parents:
                    diff_text = self.repo.git.diff(commit.parents[0].hexsha, commit.hexsha)
                else:
                    diff_text = self.repo.git.show(commit.hexsha)
            except Exception:
                diff_text = "Could not retrieve diff."

            commit_data = {
                'hexsha': commit.hexsha,
                'author_name': commit.author.name,
                'author_email': commit.author.email,
                'date': commit.authored_datetime,
                'message': commit.message.strip(),
                'diff': diff_text
            }
            commit_list.append(Commit.model_validate(commit_data))

        return commit_list

    def calculate_churn(self, branch: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, int]:
        """
        Calculates the churn (number of times each file was modified) for Python files.

        Args:
            branch: The branch to analyze.
            start_date: The start date for analysis.
            end_date: The end date for analysis.

        Returns:
            A dictionary mapping file paths to their modification count.
        """
        if branch:
            commit_spec = f"main..{branch}"
        else:
            commit_spec = self.repo.head.ref

        kwargs = {}
        if start_date:
            kwargs['after'] = start_date
        if end_date:
            kwargs['before'] = end_date

        try:
            commits = list(self.repo.iter_commits(commit_spec, **kwargs))
        except git.GitCommandError:
            commits = list(self.repo.iter_commits(branch or self.repo.head.ref, **kwargs))

        churn_data = defaultdict(int)

        for commit in commits:
            for file_path in commit.stats.files:
                if file_path.endswith('.py'):
                    churn_data[file_path] += 1

        return churn_data
