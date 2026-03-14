import os
import re
from typing import List, Dict, Any, Set
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer

class OrphanRiskInternalLinkingRule(Rule):
    @property
    def id(self) -> str:
        return "orphan_risk_internal_linking"

    @property
    def description(self) -> str:
        return "Checks if pages exist in routes but are not linked from any other page or navigation."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        page_files = analyzer.get_all_page_files()
        all_files = analyzer.get_all_component_files()

        # Build a set of route paths from page files
        routes: Set[str] = set()
        for pf in page_files:
            rel = os.path.relpath(pf, workspace)
            # Convert file path to approximate route
            route = rel.replace("src/app", "").replace("app", "").replace("src/pages", "").replace("pages", "")
            route = route.replace("page.tsx", "").replace("page.jsx", "").replace("page.ts", "").replace("page.js", "")
            route = route.replace(".tsx", "").replace(".jsx", "").replace(".ts", "").replace(".js", "")
            route = route.replace("index", "").rstrip("/").strip()
            if route == "" or route == "/":
                continue  # Skip root page
            routes.add(route)

        if not routes:
            return results

        # Check if each route segment appears as a link in any file
        linked_routes: Set[str] = set()
        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                for route in routes:
                    # Check if route path appears in href or Link
                    route_slug = route.split("/")[-1] if "/" in route else route
                    if route_slug and (route_slug in content):
                        linked_routes.add(route)
            except Exception:
                pass

        orphans = routes - linked_routes
        for orphan in orphans:
            results.append(AuditResult(
                rule_id=self.id,
                level=CheckLevel.INFO,
                message=f"Route '/{orphan}' may be an orphan page with no internal links pointing to it.",
                fix_suggestion="Add contextual internal links or navigation references to this page from other pages."
            ))
        return results
