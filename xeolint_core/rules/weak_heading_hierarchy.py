import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class WeakHeadingHierarchyRule(Rule):
    @property
    def id(self) -> str:
        return "weak_heading_hierarchy"

    @property
    def description(self) -> str:
        return "Checks if heading levels are skipped (e.g. h1 -> h3), which weakens machine parsing."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        for file_path in analyzer.get_all_page_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                headings = ContentAnalyzer.find_headings(content)
                if len(headings) < 2:
                    continue
                    
                for i in range(1, len(headings)):
                    prev_level = headings[i-1][0]
                    curr_level = headings[i][0]
                    # It's fine to go from h2 to h1 (new section), but skipping down is bad
                    if curr_level > prev_level + 1:
                        results.append(AuditResult(
                            rule_id=self.id,
                            level=CheckLevel.WARNING,
                            message=f"Heading hierarchy skips from <h{prev_level}> to <h{curr_level}> at line {headings[i][2]}.",
                            filepath=file_path,
                            fix_suggestion=f"Use <h{prev_level + 1}> instead of <h{curr_level}> to maintain proper heading hierarchy."
                        ))
                        break  # One warning per file is enough
            except Exception:
                pass
        return results
