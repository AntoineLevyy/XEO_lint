import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class MissingCanonicalRule(Rule):
    @property
    def id(self) -> str:
        return "missing_canonical"

    @property
    def description(self) -> str:
        return "Checks if a canonical URL is defined, preventing duplicate content confusion."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        for file_path in analyzer.get_all_page_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if not ContentAnalyzer.has_canonical(content):
                    results.append(AuditResult(
                        rule_id=self.id,
                        level=CheckLevel.WARNING,
                        message="No canonical URL defined for this page.",
                        filepath=file_path,
                        fix_suggestion="App Router: add alternates: { canonical: 'https://...' } to metadata. Pages Router: add <link rel='canonical' href='...'> in <Head>."
                    ))
            except Exception:
                pass
        return results
