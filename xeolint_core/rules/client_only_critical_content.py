import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class ClientOnlyCriticalContentRule(Rule):
    @property
    def id(self) -> str:
        return "client_only_critical_content"

    @property
    def description(self) -> str:
        return "Warns if important content is hidden behind 'use client' with no server-rendered equivalent."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        for file_path in analyzer.get_all_page_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if ContentAnalyzer.has_use_client(content):
                    text_len = ContentAnalyzer.estimate_text_length(content)
                    if text_len > 200:
                        results.append(AuditResult(
                            rule_id=self.id,
                            level=CheckLevel.WARNING,
                            message=f"Page marked 'use client' contains ~{text_len} chars of content. Critical text may not be visible to crawlers.",
                            filepath=file_path,
                            fix_suggestion="Move core content to a Server Component or ensure critical text is rendered in the initial HTML response."
                        ))
            except Exception:
                pass
        return results
