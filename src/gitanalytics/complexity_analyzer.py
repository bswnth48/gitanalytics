from radon.visitors import ComplexityVisitor
from radon.raw import analyze as analyze_raw
import os

class ComplexityAnalyzer:
    """
    Analyzes the cyclomatic complexity of Python files.
    """

    def analyze_files(self, repo_path: str, file_paths: list[str]) -> dict[str, int]:
        """
        Calculates the average cyclomatic complexity for a list of Python files.

        Args:
            repo_path: The absolute path to the repository, to resolve file paths.
            file_paths: A list of file paths relative to the repository root.

        Returns:
            A dictionary mapping file paths to their average cyclomatic complexity.
            Returns 0 for files that cannot be parsed or are empty.
        """
        complexity_data = {}
        for file_path in file_paths:
            full_path = os.path.join(repo_path, file_path)

            if not os.path.exists(full_path):
                complexity_data[file_path] = 0
                continue

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if not content.strip():
                    complexity_data[file_path] = 0
                    continue

                visitor = ComplexityVisitor.from_code(content)
                total_complexity = sum(f.complexity for f in visitor.functions)
                num_functions = len(visitor.functions)

                average_complexity = total_complexity / num_functions if num_functions > 0 else 0
                complexity_data[file_path] = round(average_complexity, 2)

            except Exception:
                # If radon fails to parse the file, assign a complexity of 0
                complexity_data[file_path] = 0

        return complexity_data