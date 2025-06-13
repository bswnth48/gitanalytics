import os
from collections import Counter
from typing import Optional

class LanguageDetector:
    """
    Detects the dominant programming language in a repository by analyzing file extensions.
    """
    # A simple mapping of common file extensions to languages
    EXTENSION_MAP = {
        # Python
        '.py': 'Python',
        # JavaScript / TypeScript
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'JavaScript',
        '.tsx': 'TypeScript',
        # PHP
        '.php': 'PHP',
        # Java
        '.java': 'Java',
        # Ruby
        '.rb': 'Ruby',
        # Go
        '.go': 'Go',
        # C#
        '.cs': 'C#',
        # C/C++
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C/C++',
    }

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def detect_language(self) -> Optional[str]:
        """
        Scans the repository and returns the most common programming language.

        Returns:
            The name of the dominant language (e.g., "Python"), or None if
            no supported language files are found.
        """
        file_extensions = []
        for root, _, files in os.walk(self.repo_path):
            # A simple way to exclude the .git directory
            if '.git' in root.split(os.sep):
                continue

            for file in files:
                _, extension = os.path.splitext(file)
                if extension in self.EXTENSION_MAP:
                    file_extensions.append(extension)

        if not file_extensions:
            return None

        # Count the occurrences of each extension
        extension_counts = Counter(file_extensions)

        # Get the most common extension
        most_common_extension = extension_counts.most_common(1)[0][0]

        return self.EXTENSION_MAP.get(most_common_extension)