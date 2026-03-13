import typer
from rich.console import Console
from rich.table import Table
import os

from xeolint_core import Engine
from xeolint_core.rules import (
    MissingRobotsTxtRule, 
    MissingSitemapRule, 
    MissingTitleRule,
    MissingMetaDescriptionRule,
    MissingOpenGraphRule,
    MissingTwitterCardRule
)

app = typer.Typer(help="XEOLint: A GEO and SEO linter and autofixer for Next.js")
console = Console()

@app.command()
def audit(path: str = typer.Argument(".", help="Path to the Next.js project to audit")):
    """
    Run all configured GEO and SEO rules against the project.
    """
    target_path = os.path.abspath(path)
    if not os.path.isdir(target_path):
        console.print(f"[bold red]Error:[/] Directory '{target_path}' does not exist.")
        raise typer.Exit(code=1)
        
    console.print(f"🔍 Auditing {target_path}...")
    
    engine = Engine(workspace_path=target_path)
    engine.register_rule(MissingRobotsTxtRule())
    engine.register_rule(MissingSitemapRule())
    engine.register_rule(MissingTitleRule())
    engine.register_rule(MissingMetaDescriptionRule())
    engine.register_rule(MissingOpenGraphRule())
    engine.register_rule(MissingTwitterCardRule())
    
    results = engine.audit_all()
    
    if not results:
        console.print("\n[bold green]✅ No issues found! Your Next.js app is perfectly optimized.[/]")
        return
        
    table = Table(title="Audit Results")
    table.add_column("Level", justify="left")
    table.add_column("Rule", justify="left")
    table.add_column("Message", justify="left")
    table.add_column("File", justify="left")
    table.add_column("Suggested Fix", justify="left")
    
    for res in results:
        # 1. Clean up Enum print
        level_str = res.level.value if hasattr(res.level, 'value') else str(res.level)
        
        if level_str == "ERROR":
            level_color = "red"
        elif level_str == "WARNING":
            level_color = "yellow"
        elif level_str == "PASS":
            level_color = "green"
        else:
            level_color = "cyan"
        
        # 2. Shorten paths to be relative
        rel_path = "Global"
        if res.filepath:
            try:
                rel_path = os.path.relpath(res.filepath, target_path)
            except ValueError:
                rel_path = res.filepath
                
            # 3. Add explicit route hints for pages
            if "page" in rel_path or "route" in rel_path:
                route = rel_path.replace("src/app", "").replace("app", "").replace("pages", "").replace("page.tsx", "").replace("page.jsx", "")
                route = route if route else "/"
                rel_path = f"{rel_path} (route: {route})"
                
        table.add_row(
            f"[{level_color}]{level_str}[/]",
            res.rule_id,
            res.message,
            rel_path,
            res.fix_suggestion or "-"
        )
        
    console.print(table)
    
@app.command()
def fix(path: str = typer.Argument(".", help="Path to the Next.js project to fix")):
    """
    Automatically fix safe GEO and SEO issues in the project.
    """
    target_path = os.path.abspath(path)
    console.print(f"🛠️ Attempting auto-fixes on {target_path}...")
    
    engine = Engine(workspace_path=target_path)
    engine.register_rule(MissingRobotsTxtRule())
    engine.register_rule(MissingSitemapRule())
    engine.register_rule(MissingTitleRule())
    engine.register_rule(MissingMetaDescriptionRule())
    engine.register_rule(MissingOpenGraphRule())
    engine.register_rule(MissingTwitterCardRule())
    
    results = engine.fix_all()
    
    if not results:
        console.print("\n[bold green]✨ No fixable issues found.[/]")
        return
        
    table = Table(title="Fix Results")
    table.add_column("Status", justify="left")
    table.add_column("Rule", justify="left")
    table.add_column("Message", justify="left")
    table.add_column("File", justify="left")
    
    for res in results:
        status_str = res.status.value if hasattr(res.status, 'value') else str(res.status)
        
        if status_str == "FIXED":
            status_color = "green"
        elif status_str == "NOT_APPLICABLE":
            status_color = "cyan"
            status_str = "SUGGESTION_ONLY"
        else:
            status_color = "yellow"
        
        rel_path = "Global"
        if res.filepath:
            try:
                 rel_path = os.path.relpath(res.filepath, target_path)
            except ValueError:
                 rel_path = res.filepath
                 
        table.add_row(
            f"[{status_color}]{status_str}[/]",
            res.rule_id,
            res.message,
            rel_path
        )
        
    console.print(table)

if __name__ == "__main__":
    app()
