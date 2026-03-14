import os
import re
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

VAGUE_PATTERNS = [
    r'^build\s+better',
    r'^the\s+future',
    r'^welcome\s+to',
    r'^get\s+started',
    r'^introducing',
    r'^discover\s+the',
    r'^unlock\s+the',
    r'^transform\s+your',
    r'^revolutionize',
    r'^empower',
    r'^supercharge',
    r'^next[\s-]gen',
]

class UnclearPagePurposeRule(Rule):
    @property
    def id(self) -> str:
        return "unclear_page_purpose"

    @property
    def description(self) -> str:
        return "Checks if the page H1 or hero copy clearly states what the product/page is about."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        for file_path in analyzer.get_all_page_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                h1_text = ContentAnalyzer.get_h1_text(content)
                if h1_text:
                    for pattern in VAGUE_PATTERNS:
                        if re.search(pattern, h1_text, re.IGNORECASE):
                            results.append(AuditResult(
                                rule_id=self.id,
                                level=CheckLevel.INFO,
                                message=f"H1 text '{h1_text}' may be too vague for GEO. AI systems benefit from explicit purpose statements.",
                                filepath=file_path,
                                fix_suggestion="Rewrite H1 to clearly state what the product/page is, who it's for, and what problem it solves."
                            ))
                            break
            except Exception:
                pass
        return results
