import os
from typing import List, Optional

class NextProjectAnalyzer:
    """Utility class to analyze the structure of a Next.js project."""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        
    @property
    def has_app_router(self) -> bool:
        """Determines if the project uses the App Router."""
        # Check both src/app and root app/
        return (
            os.path.isdir(os.path.join(self.workspace_path, "app")) or
            os.path.isdir(os.path.join(self.workspace_path, "src", "app"))
        )
        
    @property
    def has_pages_router(self) -> bool:
        """Determines if the project uses the Pages Router."""
        return (
            os.path.isdir(os.path.join(self.workspace_path, "pages")) or
            os.path.isdir(os.path.join(self.workspace_path, "src", "pages"))
        )
        
    @property
    def app_router_path(self) -> Optional[str]:
        app_path = os.path.join(self.workspace_path, "app")
        if os.path.isdir(app_path):
            return app_path
        src_app_path = os.path.join(self.workspace_path, "src", "app")
        if os.path.isdir(src_app_path):
            return src_app_path
        return None
        
    @property
    def pages_router_path(self) -> Optional[str]:
        pages_path = os.path.join(self.workspace_path, "pages")
        if os.path.isdir(pages_path):
            return pages_path
        src_pages_path = os.path.join(self.workspace_path, "src", "pages")
        if os.path.isdir(src_pages_path):
            return src_pages_path
        return None

    def get_all_page_files(self) -> List[str]:
        """Returns a list of all route entry files (page.tsx, page.jsx, pages/*.tsx)."""
        files = []
        app_path = self.app_router_path
        if app_path:
            for root, _, filenames in os.walk(app_path):
                for filename in filenames:
                    if filename.startswith("page.") and filename.endswith((".tsx", ".jsx", ".js", ".ts")):
                        files.append(os.path.join(root, filename))
                        
        pages_path = self.pages_router_path
        if pages_path:
             for root, _, filenames in os.walk(pages_path):
                 if "api" in root.split(os.sep): 
                     continue # skip api routes
                 for filename in filenames:
                     if filename.endswith((".tsx", ".jsx", ".js", ".ts")) and not filename.startswith("_"):
                         files.append(os.path.join(root, filename))
        
        return files

import re

class MetadataExtractor:
    """Extracts metadata configurations from TSX/JSX file contents."""
    
    @staticmethod
    def has_app_router_metadata(file_content: str) -> bool:
        """Checks if export const metadata = {} exists."""
        pattern = r'export\s+const\s+metadata\s*(:\s*Metadata\s*)?=\s*\{'
        return bool(re.search(pattern, file_content))

    @staticmethod
    def has_app_router_title(file_content: str) -> bool:
        """Checks if title is defined inside metadata."""
        if not MetadataExtractor.has_app_router_metadata(file_content):
            return False
        
        # Check for standard string title or object title
        pattern_str = r'title\s*:\s*[\'"`].*?[\'"`]'
        pattern_obj = r'title\s*:\s*\{'
        
    @staticmethod
    def has_app_router_description(file_content: str) -> bool:
        """Checks if description is defined inside metadata."""
        if not MetadataExtractor.has_app_router_metadata(file_content):
            return False
            
        pattern_str = r'description\s*:\s*[\'"`].*?[\'"`]'
        pattern_obj = r'description\s*:\s*\{'
        return bool(re.search(pattern_str, file_content) or re.search(pattern_obj, file_content))

    @staticmethod
    def has_app_router_open_graph(file_content: str) -> bool:
        """Checks if openGraph is defined inside metadata."""
        if not MetadataExtractor.has_app_router_metadata(file_content):
            return False
        return bool(re.search(r'openGraph\s*:\s*\{', file_content))
        
    @staticmethod
    def has_app_router_twitter(file_content: str) -> bool:
        """Checks if twitter is defined inside metadata."""
        if not MetadataExtractor.has_app_router_metadata(file_content):
            return False
        return bool(re.search(r'twitter\s*:\s*\{', file_content))
        
    @staticmethod
    def has_pages_router_head_title(file_content: str) -> bool:
        """Checks if <title> is defined inside <Head>."""
        pattern = r'<Head>[\s\S]*?<title>[\s\S]*?</title>[\s\S]*?</Head>'
        return bool(re.search(pattern, file_content))
