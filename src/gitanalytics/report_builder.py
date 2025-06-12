import json
from datetime import datetime
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader
import os

from .git_analyzer import Commit

class ReportBuilder:
    """
    Builds reports from analysis data in various formats.
    """
    def __init__(self, repo_path: str, start_date: str, end_date: str):
        """
        Initializes the ReportBuilder.
        """
        self.repo_path = os.path.abspath(repo_path)
        self.start_date = start_date or "First Commit"
        self.end_date = end_date or datetime.now().strftime("%Y-%m-%d")

        # Set up Jinja2 environment
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def _generate_report_filename(self, extension: str) -> str:
        """Creates a unique report filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"git_analytics_report_{timestamp}.{extension}"

    def _format_date(self, date_obj) -> str:
        """Helper to format date objects or date strings consistently."""
        if isinstance(date_obj, str):
            # Attempt to parse ISO format string
            return datetime.fromisoformat(date_obj).strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(date_obj, datetime):
            return date_obj.strftime('%Y-%m-%d %H:%M:%S')
        return "Unknown Date"

    def _prepare_context(self, categorized_commits: Dict[str, List[Dict]], executive_summary: str) -> Dict:
        """Prepares the context dictionary for rendering templates."""
        # Process commits to ensure dates are strings for the template
        for category, results in categorized_commits.items():
            for result in results:
                # The commit data is now nested under the 'commit' key
                commit_data = result['commit']
                commit_data['date_str'] = self._format_date(commit_data['date'])

        return {
            "repo_path": self.repo_path,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "categorized_commits": categorized_commits,
            "executive_summary": executive_summary
        }

    def generate_markdown_report(self, categorized_commits: Dict[str, List[Dict]], executive_summary: str) -> str:
        """
        Generates a Markdown report from categorized data.
        """
        template = self.env.get_template('report.md.j2')

        context = self._prepare_context(categorized_commits, executive_summary)
        rendered_report = template.render(context)

        filename = self._generate_report_filename("md")
        with open(filename, "w") as f:
            f.write(rendered_report)
        return filename

    def generate_json_report(self, categorized_commits: Dict[str, List[Dict]], executive_summary: str) -> str:
        """
        Generates a JSON report from categorized data.
        """
        # Flatten the categorized structure for the JSON report for easier parsing
        flat_results = []
        total_commits = 0
        for category, items in categorized_commits.items():
            total_commits += len(items)
            for item in items:
                commit = item['commit']
                flat_results.append({
                    'category': category,
                    'commit_hash': commit.commit_hash,
                    'author': commit.author_name,
                    'date': commit.date.isoformat(),
                    'message': commit.message,
                    'summary': item['summary']
                })

        report_data = {
            'report_metadata': {
                'repo_path': self.repo_path,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'generated_at': datetime.now().isoformat(),
                'commit_count': total_commits
            },
            'executive_summary': executive_summary,
            'analysis_results': flat_results
        }

        filename = self._generate_report_filename("json")
        with open(filename, "w") as f:
            json.dump(report_data, f, indent=2)
        return filename
