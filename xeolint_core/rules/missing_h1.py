import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class MissingH1Rule(Rule):
    @property
    def id(self) -> str:
        return "missing_h1"

    @property
    def description(self) -> str:
        return "Checks if the page has an <h1> tag, which clarifies the primary concept for SEO and GEO."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        for file_path in analyzer.get_all_page_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                headings = ContentAnalyzer.find_headings(content)
                h1s = [h for h in headings if h[0] == 1]
                if not h1s:
                    results.append(AuditResult(
                        rule_id=self.id,
                        level=CheckLevel.ERROR,
                        message="No <h1> tag found on this page.",
                        filepath=file_path,
                        fix_suggestion="Add a single, clear <h1> near the top of your main content describing the page topic."
                    ))
            except Exception:
                pass
        return results
