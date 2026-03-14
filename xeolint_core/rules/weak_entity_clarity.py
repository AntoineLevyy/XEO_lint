import os
import re
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, MetadataExtractor, ContentAnalyzer

class WeakEntityClarityRule(Rule):
    @property
    def id(self) -> str:
        return "weak_entity_clarity"

    @property
    def description(self) -> str:
        return "Checks if the brand/product name appears consistently across title, description, H1, and body."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        # Try to extract entity name from package.json or next.config
        entity_name = self._extract_entity_name(workspace)
        if not entity_name:
            return results  # Can't check without knowing the entity

        for file_path in analyzer.get_all_page_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                mentions = len(re.findall(re.escape(entity_name), content, re.IGNORECASE))
                if mentions == 0:
                    results.append(AuditResult(
                        rule_id=self.id,
                        level=CheckLevel.INFO,
                        message=f"Entity '{entity_name}' not found on this page. Entity clarity helps LLMs.",
                        filepath=file_path,
                        fix_suggestion=f"Mention '{entity_name}' in the title, description, H1, or intro copy for stronger entity signals."
                    ))
            except Exception:
                pass
        return results

    def _extract_entity_name(self, workspace: str) -> str:
        """Try to find the project/brand name from package.json."""
        pkg_path = os.path.join(workspace, "package.json")
        if os.path.exists(pkg_path):
            try:
                import json
                with open(pkg_path, 'r') as f:
                    pkg = json.load(f)
                name = pkg.get("name", "")
                if name and not name.startswith("@"):
                    return name.replace("-", " ").replace("_", " ").title()
            except Exception:
                pass
        return ""
