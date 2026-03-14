import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import os

from xeolint_core import Engine
from xeolint_core.rules import ALL_RULES

app = typer.Typer(help="XEOLint: A GEO and SEO linter and autofixer for Next.js")
console = Console()


def _create_engine(target_path: str) -> Engine:
    """Create an engine with all rules registered."""
    engine = Engine(workspace_path=target_path)
    for rule_cls in ALL_RULES:
        engine.register_rule(rule_cls())
    return engine


def _level_color(level_str: str) -> str:
    if level_str == "ERROR":
        return "red"
    elif level_str == "WARNING":
        return "yellow"
    elif level_str == "PASS":
        return "green"
    return "cyan"


def _rel_path(filepath: str, target_path: str) -> str:
    if not filepath:
        return "Global"
    try:
        return os.path.relpath(filepath, target_path)
    except ValueError:
        return filepath


def _format_block(res, target_path: str):
    """Print a single audit result as a readable block."""
    level_str = res.level.value if hasattr(res.level, 'value') else str(res.level)
    color = _level_color(level_str)
    rel = _rel_path(res.filepath, target_path)

    console.print(f"[bold {color}]{level_str}[/]  [bold]{res.rule_id}[/]")
    console.print(f"  File: {rel}")
    console.print(f"  Message: {res.message}")
    if res.fix_suggestion and res.fix_suggestion != "-":
        console.print(f"  Fix: [dim]{res.fix_suggestion}[/]")
    console.print()


def _format_table(results, target_path: str):
    """Print audit results as a Rich table."""
    table = Table(title="Audit Results")
    table.add_column("Level", justify="left")
    table.add_column("Rule", justify="left")
    table.add_column("Message", justify="left")
    table.add_column("File", justify="left")
    table.add_column("Suggested Fix", justify="left")

    for res in results:
        level_str = res.level.value if hasattr(res.level, 'value') else str(res.level)
        color = _level_color(level_str)
        rel = _rel_path(res.filepath, target_path)

        if "page" in rel or "route" in rel:
            route = rel.replace("src/app", "").replace("app", "").replace("pages", "").replace("page.tsx", "").replace("page.jsx", "")
            route = route if route else "/"
            rel = f"{rel} (route: {route})"

        table.add_row(
            f"[{color}]{level_str}[/]",
            res.rule_id,
            res.message,
            rel,
            res.fix_suggestion or "-"
        )

    console.print(table)


@app.command()
def audit(
    path: str = typer.Argument(".", help="Path to the Next.js project to audit"),
    table: bool = typer.Option(False, "--table", help="Display results as a table instead of blocks")
):
    """
    Run all configured GEO and SEO rules against the project.
    """
    target_path = os.path.abspath(path)
    if not os.path.isdir(target_path):
        console.print(f"[bold red]Error:[/] Directory '{target_path}' does not exist.")
        raise typer.Exit(code=1)

    console.print(f"\n🔍 [bold]XEOLint[/] — Auditing [cyan]{target_path}[/]\n")

    engine = _create_engine(target_path)
    results = engine.audit_all()

    if not results:
        console.print("[bold green]✅ No issues found! Your Next.js app is perfectly optimized.[/]")
        return

    # Split into issues and passes
    issues = [r for r in results if r.level.value != "PASS"]
    passes = [r for r in results if r.level.value == "PASS"]

    if table:
        _format_table(results, target_path)
    else:
        # Block format (default)
        if issues:
            for res in issues:
                _format_block(res, target_path)

        if passes:
            pass_names = ", ".join(set(r.rule_id for r in passes))
            console.print(f"[bold green]✅ Passed:[/] {pass_names}\n")

    # Summary
    error_count = sum(1 for r in results if r.level.value == "ERROR")
    warn_count = sum(1 for r in results if r.level.value == "WARNING")
    info_count = sum(1 for r in results if r.level.value == "INFO")
    pass_count = len(passes)

    console.print(
        f"[bold]Summary:[/] "
        f"[red]{error_count} errors[/] · "
        f"[yellow]{warn_count} warnings[/] · "
        f"[cyan]{info_count} info[/] · "
        f"[green]{pass_count} passed[/]"
    )


@app.command()
def fix(path: str = typer.Argument(".", help="Path to the Next.js project to fix")):
    """
    Automatically fix safe GEO and SEO issues in the project.
    """
    target_path = os.path.abspath(path)
    console.print(f"\n🛠️ [bold]XEOLint[/] — Fixing [cyan]{target_path}[/]\n")

    engine = _create_engine(target_path)
    results = engine.fix_all()

    if not results:
        console.print("[bold green]✨ No fixable issues found.[/]")
        return

    for res in results:
        status_str = res.status.value if hasattr(res.status, 'value') else str(res.status)

        if status_str == "FIXED":
            color = "green"
            icon = "✅"
        elif status_str == "NOT_APPLICABLE":
            color = "cyan"
            status_str = "SUGGESTION_ONLY"
            icon = "💡"
        else:
            color = "yellow"
            icon = "⚠️"

        rel = _rel_path(res.filepath, target_path)
        console.print(f"{icon} [{color}]{status_str}[/]  [bold]{res.rule_id}[/]")
        console.print(f"  File: {rel}")
        console.print(f"  {res.message}")
        console.print()


if __name__ == "__main__":
    app()
