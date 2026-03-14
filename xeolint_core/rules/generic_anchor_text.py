import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class GenericAnchorTextRule(Rule):
    @property
    def id(self) -> str:
        return "generic_anchor_text"

    @property
    def description(self) -> str:
        return "Checks for anchor tags with generic text like 'click here' or 'learn more' which give poor semantic clues."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        for file_path in analyzer.get_all_component_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                generic = ContentAnalyzer.find_generic_anchors(content)
                for text, line_num in generic:
                    results.append(AuditResult(
                        rule_id=self.id,
                        level=CheckLevel.INFO,
                        message=f"Generic anchor text '{text}' found at line {line_num}.",
                        filepath=file_path,
                        line_number=line_num,
                        fix_suggestion=f"Replace '{text}' with a specific descriptive label, e.g. 'View pricing plans' or 'Read the case study'."
                    ))
            except Exception:
                pass
        return results
