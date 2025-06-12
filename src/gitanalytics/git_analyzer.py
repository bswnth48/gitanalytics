import git
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

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
    Analyzes a Git repository to extract commit information.
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

    def get_commits(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Commit]:
        """
        Extracts commits from the repository within a given date range.

        Args:
            start_date: The start date in YYYY-MM-DD format.
            end_date: The end date in YYYY-MM-DD format.

        Returns:
            A list of Commit objects.
        """
        kwargs = {}
        if start_date:
            kwargs['after'] = start_date
        if end_date:
            kwargs['before'] = end_date

        commits_iter = self.repo.iter_commits(**kwargs)

        commit_list = []
        for commit in commits_iter:
            # Get the diff for the commit
            try:
                if commit.parents:
                    # Diff against the first parent for simplicity
                    diff_text = self.repo.git.diff(commit.parents[0].hexsha, commit.hexsha)
                else:
                    # This is the initial commit, diff against the empty tree
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
