import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class MissingJsonLdRule(Rule):
    @property
    def id(self) -> str:
        return "missing_json_ld"

    @property
    def description(self) -> str:
        return "Checks if JSON-LD structured data exists, which is an excellent signal for entities and page meaning."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        all_files = analyzer.get_all_page_files() + analyzer.get_all_layout_files()
        found_json_ld = False

        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if ContentAnalyzer.has_json_ld(content):
                    found_json_ld = True
                    break
            except Exception:
                pass

        if not found_json_ld:
            results.append(AuditResult(
                rule_id=self.id,
                level=CheckLevel.WARNING,
                message="No JSON-LD structured data found in any page or layout.",
                fix_suggestion="Add a <script type='application/ld+json'> block with Organization, WebSite, or page-specific schema."
            ))
        return results
