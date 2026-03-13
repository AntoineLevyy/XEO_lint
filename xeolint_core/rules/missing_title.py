import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, FixResult, CheckLevel, FixStatus
from xeolint_core.parsers import NextProjectAnalyzer, MetadataExtractor

class MissingTitleRule(Rule):
    @property
    def id(self) -> str:
        return "missing_title"
        
    @property
    def description(self) -> str:
        return "Checks if a title is defined for the page route, either via export const metadata or <Head>."
        
    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        page_files = analyzer.get_all_page_files()
        
        results = []
        
        for file_path in page_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Very basic heuristic: if it's in the app directory
                is_app_router = "app" in file_path.split(os.sep)
                
                if is_app_router:
                    # Check for Metadata Definition
                    if not MetadataExtractor.has_app_router_metadata(content):
                        results.append(AuditResult(
                            rule_id=self.id,
                            level=CheckLevel.ERROR,
                            message="No metadata exported in this page. Missing Title.",
                            filepath=file_path,
                            fix_suggestion="Export a metadata object with a 'title' key."
                        ))
                    elif not MetadataExtractor.has_app_router_title(content):
                        results.append(AuditResult(
                            rule_id=self.id,
                            level=CheckLevel.ERROR,
                            message="Metadata exported, but no title defined. Missing Title.",
                            filepath=file_path,
                            fix_suggestion="Add a 'title' key to the exported metadata object."
                        ))
                else:
                    # Pages Router logic
                    if not MetadataExtractor.has_pages_router_head_title(content):
                         results.append(AuditResult(
                            rule_id=self.id,
                            level=CheckLevel.ERROR,
                            message="No <title> found inside <Head> on this page route.",
                            filepath=file_path,
                            fix_suggestion="Inject a <title> element inside the Next.js <Head> component."
                        ))
            except Exception as e:
                # Silently ignore unreadable files for now
                pass
                
        return results
        
    def fix(self, context: Dict[str, Any], audit_results: List[AuditResult]) -> List[FixResult]:
        # Autofix for missing title is risky without AST rewriting for MVP.
        # So we suggest manual fix or fallback returning NOT_APPLICABLE for now.
        return super().fix(context, audit_results)
