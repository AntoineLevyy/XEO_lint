import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class MultipleH1Rule(Rule):
    @property
    def id(self) -> str:
        return "multiple_h1"

    @property
    def description(self) -> str:
        return "Checks if multiple <h1> tags exist on one page, which weakens the main topical signal."

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
                if len(h1s) > 1:
                    results.append(AuditResult(
                        rule_id=self.id,
                        level=CheckLevel.WARNING,
                        message=f"Found {len(h1s)} <h1> tags. Keep one primary <h1> and downgrade others to <h2>.",
                        filepath=file_path,
                        fix_suggestion="Keep only one <h1> for the primary page topic. Change additional <h1> tags to <h2> or lower."
                    ))
            except Exception:
                pass
        return results
