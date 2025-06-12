import pytest
import git
import tempfile
import shutil
from pathlib import Path

@pytest.fixture(scope="function")
def test_repo():
    """
    Pytest fixture to create a temporary Git repository for testing.

    This fixture creates a new directory, initializes a Git repository,
    makes a few commits, and then yields the path to the repository.
    After the test function completes, it cleans up by deleting the
    temporary directory.

    Yields:
        Path: The path to the temporary Git repository.
    """
    repo_dir = Path(tempfile.mkdtemp())
    repo = git.Repo.init(repo_dir)

    # Set a specific author for the test commits
    with repo.config_writer() as cw:
        cw.set_value("user", "name", "Test User").release()
        cw.set_value("user", "email", "test@example.com").release()

    # Create and commit some files
    (repo_dir / "file1.txt").write_text("This is the first file.")
    repo.index.add(["file1.txt"])
    repo.index.commit("feat: Add first file")

    (repo_dir / "file2.txt").write_text("This is the second file.")
    repo.index.add(["file2.txt"])
    repo.index.commit("fix: Add second file")

    (repo_dir / "file1.txt").write_text("This is the first file, modified.")
    repo.index.add(["file1.txt"])
    repo.index.commit("refactor: Modify first file")

    yield repo_dir

    # Teardown: remove the temporary directory
    shutil.rmtree(repo_dir)