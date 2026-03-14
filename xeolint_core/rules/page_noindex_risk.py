import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class PageNoindexRiskRule(Rule):
    @property
    def id(self) -> str:
        return "page_noindex_risk"

    @property
    def description(self) -> str:
        return "Checks if pages accidentally have noindex directives, which may prevent indexing by search and AI."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        for file_path in analyzer.get_all_page_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if ContentAnalyzer.has_noindex(content):
                    results.append(AuditResult(
                        rule_id=self.id,
                        level=CheckLevel.WARNING,
                        message="Page has noindex directive. It may be excluded from search and AI crawlers.",
                        filepath=file_path,
                        fix_suggestion="Remove 'index: false' from robots metadata or 'noindex' from meta content, unless intentional."
                    ))
            except Exception:
                pass
        return results
