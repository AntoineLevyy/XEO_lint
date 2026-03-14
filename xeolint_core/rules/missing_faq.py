import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class MissingFaqRule(Rule):
    @property
    def id(self) -> str:
        return "missing_faq_or_structured_qa"

    @property
    def description(self) -> str:
        return "Checks if FAQ sections or FAQ schema exist, which map naturally to question-answer retrieval."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        all_files = analyzer.get_all_page_files() + analyzer.get_all_layout_files()
        found_faq = False

        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if ContentAnalyzer.has_faq_section(content):
                    found_faq = True
                    break
            except Exception:
                pass

        if not found_faq:
            results.append(AuditResult(
                rule_id=self.id,
                level=CheckLevel.INFO,
                message="No FAQ section or FAQ schema found. FAQ structure helps AI question-answer retrieval.",
                fix_suggestion="Add an FAQ section with explicit Q&A blocks and optionally FAQPage JSON-LD schema."
            ))
        return results
