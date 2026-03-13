import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, FixResult, CheckLevel, FixStatus
from xeolint_core.parsers import NextProjectAnalyzer, MetadataExtractor

class MissingOpenGraphRule(Rule):
    @property
    def id(self) -> str:
        return "missing_open_graph"
        
    @property
    def description(self) -> str:
        return "Checks if Open Graph metadata is provided to improve social previews and structured signals."
        
    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        page_files = analyzer.get_all_page_files()
        
        results = []
        
        for file_path in page_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                is_app_router = "app" in file_path.split(os.sep)
                
                if is_app_router:
                    if MetadataExtractor.has_app_router_metadata(content) and not MetadataExtractor.has_app_router_open_graph(content):
                        results.append(AuditResult(
                            rule_id=self.id,
                            level=CheckLevel.WARNING,
                            message="Metadata exported, but no OpenGraph definition found.",
                            filepath=file_path,
                            fix_suggestion="Add an 'openGraph' object with title and description to your exported metadata."
                        ))
                else:
                    if "<Head>" in content and "property=\"og:" not in content and "property='og:" not in content:
                         results.append(AuditResult(
                            rule_id=self.id,
                            level=CheckLevel.WARNING,
                            message="No OpenGraph <meta property=\"og:...\"> found inside <Head>.",
                            filepath=file_path,
                            fix_suggestion="Add <meta property='og:title' content='...'> inside <Head>."
                        ))
            except Exception:
                pass
                
        return results
