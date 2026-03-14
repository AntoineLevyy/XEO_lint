import os
import re
from typing import List, Optional, Tuple

class NextProjectAnalyzer:
    """Utility class to analyze the structure of a Next.js project."""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        
    @property
    def has_app_router(self) -> bool:
        """Determines if the project uses the App Router."""
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

    def get_all_component_files(self) -> List[str]:
        """Returns all .tsx/.jsx/.js/.ts files in the project (excluding node_modules, .next)."""
        files = []
        exclude_dirs = {"node_modules", ".next", ".git", "__pycache__", ".venv", "dist", "build"}
        for root, dirs, filenames in os.walk(self.workspace_path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for filename in filenames:
                if filename.endswith((".tsx", ".jsx", ".js", ".ts")):
                    files.append(os.path.join(root, filename))
        return files

    def get_all_layout_files(self) -> List[str]:
        """Returns all layout.tsx/layout.jsx files in the app directory."""
        files = []
        app_path = self.app_router_path
        if app_path:
            for root, _, filenames in os.walk(app_path):
                for filename in filenames:
                    if filename.startswith("layout.") and filename.endswith((".tsx", ".jsx", ".js", ".ts")):
                        files.append(os.path.join(root, filename))
        return files


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
        pattern_str = r'title\s*:\s*[\'"`].*?[\'"`]'
        pattern_obj = r'title\s*:\s*\{'
        return bool(re.search(pattern_str, file_content) or re.search(pattern_obj, file_content))

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


class ContentAnalyzer:
    """Analyzes HTML/JSX content for structural and semantic checks."""

    @staticmethod
    def find_headings(file_content: str) -> List[Tuple[int, str, int]]:
        """
        Returns a list of (heading_level, heading_text, line_number).
        Finds <h1>, <h2>, ..., <h6> tags.
        """
        headings = []
        for i, line in enumerate(file_content.splitlines(), 1):
            matches = re.findall(r'<h([1-6])[^>]*>(.*?)</h\1>', line, re.IGNORECASE)
            for level, text in matches:
                clean_text = re.sub(r'<[^>]+>', '', text).strip()
                headings.append((int(level), clean_text, i))
        # Also catch multi-line or JSX expression headings
        for match in re.finditer(r'<h([1-6])[^>]*>', file_content):
            level = int(match.group(1))
            line_num = file_content[:match.start()].count('\n') + 1
            # Avoid duplicates
            if not any(h[2] == line_num for h in headings):
                headings.append((level, "", line_num))
        return sorted(headings, key=lambda x: x[2])

    @staticmethod
    def has_semantic_landmark(file_content: str, tag: str) -> bool:
        """Check if a semantic landmark tag exists (e.g. <main>, <nav>, <footer>)."""
        return bool(re.search(rf'<{tag}[\s>]', file_content, re.IGNORECASE))

    @staticmethod
    def find_images_missing_alt(file_content: str) -> List[Tuple[str, int]]:
        """Find <img> or <Image (next/image) tags missing meaningful alt text."""
        results = []
        for i, line in enumerate(file_content.splitlines(), 1):
            # Match <img or <Image tags
            img_matches = re.finditer(r'<(?:img|Image)\b([^>]*?)/?>', line, re.IGNORECASE)
            for match in img_matches:
                attrs = match.group(1)
                # Check for missing alt, empty alt, or placeholder alt
                has_alt = re.search(r'alt\s*=\s*[\'"`](.+?)[\'"`]', attrs)
                if not has_alt:
                    results.append(("missing", i))
                elif has_alt.group(1).strip().lower() in ("", "image", "img", "photo", "picture", "placeholder"):
                    results.append(("placeholder", i))
        return results

    @staticmethod
    def has_json_ld(file_content: str) -> bool:
        """Check if JSON-LD structured data exists."""
        return bool(re.search(r'application/ld\+json', file_content))

    @staticmethod
    def has_use_client(file_content: str) -> bool:
        """Check if the file starts with 'use client' directive."""
        stripped = file_content.lstrip()
        return stripped.startswith('"use client"') or stripped.startswith("'use client'")

    @staticmethod
    def find_generic_anchors(file_content: str) -> List[Tuple[str, int]]:
        """Find anchor tags with generic text like 'click here', 'learn more'."""
        generic_texts = [
            "click here", "read more", "learn more", "here", "more",
            "link", "this", "go", "see more", "view more", "details"
        ]
        results = []
        for i, line in enumerate(file_content.splitlines(), 1):
            # Match <a> or <Link> content
            anchor_matches = re.finditer(r'<(?:a|Link)\b[^>]*>(.*?)</(?:a|Link)>', line, re.IGNORECASE)
            for match in anchor_matches:
                text = re.sub(r'<[^>]+>', '', match.group(1)).strip().lower()
                if text in generic_texts:
                    results.append((text, i))
        return results

    @staticmethod 
    def estimate_text_length(file_content: str) -> int:
        """Rough estimate of visible text content length in a component."""
        # Strip JSX tags, imports, exports
        text = re.sub(r'<[^>]+>', ' ', file_content)
        text = re.sub(r'import\s+.*?;', '', text)
        text = re.sub(r'export\s+.*?;', '', text)
        text = re.sub(r'\{[^}]*\}', '', text)
        text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        return len(text.strip())

    @staticmethod
    def has_canonical(file_content: str) -> bool:
        """Check if canonical URL is defined."""
        # App Router: alternates: { canonical: ... }
        if re.search(r'alternates\s*:\s*\{', file_content) and re.search(r'canonical\s*:', file_content):
            return True
        # Pages Router: <link rel="canonical"
        if re.search(r'rel\s*=\s*[\'"]canonical[\'"]', file_content):
            return True
        return False

    @staticmethod
    def has_noindex(file_content: str) -> bool:
        """Check if page has noindex directives."""
        # App Router: robots: { index: false }
        if re.search(r'index\s*:\s*false', file_content):
            return True
        # Meta tag
        if re.search(r'content\s*=\s*[\'"].*?noindex.*?[\'"]', file_content, re.IGNORECASE):
            return True
        return False

    @staticmethod
    def get_h1_text(file_content: str) -> Optional[str]:
        """Extract h1 text content."""
        match = re.search(r'<h1[^>]*>(.*?)</h1>', file_content, re.DOTALL | re.IGNORECASE)
        if match:
            return re.sub(r'<[^>]+>', '', match.group(1)).strip()
        return None

    @staticmethod
    def has_faq_section(file_content: str) -> bool:
        """Check if FAQ section or FAQ schema exists."""
        if re.search(r'FAQPage', file_content):
            return True
        if re.search(r'<(section|div)[^>]*(?:id|class)\s*=\s*[\'"][^\'"]*faq[^\'"]*[\'"]', file_content, re.IGNORECASE):
            return True
        # Check for Q&A patterns
        faq_keywords = re.findall(r'(?:question|faq|q&a|asked)', file_content, re.IGNORECASE)
        return len(faq_keywords) >= 2
