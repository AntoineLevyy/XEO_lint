import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class MissingAltTextRule(Rule):
    @property
    def id(self) -> str:
        return "missing_alt_text"

    @property
    def description(self) -> str:
        return "Checks if images (<img> or next/image) have meaningful alt text."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        for file_path in analyzer.get_all_component_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                missing = ContentAnalyzer.find_images_missing_alt(content)
                for kind, line_num in missing:
                    msg = "Image missing alt text." if kind == "missing" else "Image has placeholder alt text."
                    results.append(AuditResult(
                        rule_id=self.id,
                        level=CheckLevel.WARNING,
                        message=f"{msg} (line {line_num})",
                        filepath=file_path,
                        line_number=line_num,
                        fix_suggestion="Add a descriptive alt attribute that explains the image content and context."
                    ))
            except Exception:
                pass
        return results
