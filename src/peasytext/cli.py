"""peasytext CLI — Text processing from the command line.

Usage::

    peasytext case "hello world" --target pascal
    peasytext slug "Hello World!"
    peasytext count "Hello world. How are you?"
    echo "line b\\nline a" | peasytext sort
    peasytext base64 encode "Hello"
    peasytext lorem 3 --unit paragraphs
"""

from __future__ import annotations

import sys

import typer
from rich.console import Console
from rich.table import Table

from peasytext import engine

app = typer.Typer(
    name="peasytext",
    help="Text processing toolkit — 15 tools from peasytext.com",
    no_args_is_help=True,
)
console = Console()


def _read_input(text: str | None) -> str:
    """Read from argument or stdin."""
    if text:
        return text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    console.print("[red]Error: provide text as argument or pipe via stdin[/red]")
    raise typer.Exit(1)


@app.command()
def case(
    text: str | None = typer.Argument(None, help="Text to convert (or pipe via stdin)"),
    target: str = typer.Option("upper", "--target", "-t", help="Target case"),
) -> None:
    """Convert text between cases (upper, lower, title, camel, snake, kebab, etc.)."""
    content = _read_input(text)
    result = engine.to_case(content, target)  # type: ignore[arg-type]
    console.print(result)


@app.command()
def slug(
    text: str | None = typer.Argument(None, help="Text to slugify (or pipe via stdin)"),
    separator: str = typer.Option("-", "--sep", "-s", help="Separator character"),
    max_length: int = typer.Option(0, "--max-length", "-m", help="Max slug length (0=unlimited)"),
) -> None:
    """Convert text to a URL-friendly slug."""
    content = _read_input(text)
    result = engine.slugify(content, separator=separator, max_length=max_length)
    console.print(result)


@app.command()
def count(
    text: str | None = typer.Argument(None, help="Text to analyze (or pipe via stdin)"),
    wpm: int = typer.Option(200, "--wpm", help="Words per minute for reading time"),
) -> None:
    """Count characters, words, sentences, paragraphs, and lines."""
    content = _read_input(text)
    stats = engine.count_text(content, words_per_minute=wpm)

    table = Table(title="Text Statistics", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green", justify="right")
    table.add_row("Characters", str(stats.characters))
    table.add_row("Characters (no spaces)", str(stats.characters_no_spaces))
    table.add_row("Words", str(stats.words))
    table.add_row("Sentences", str(stats.sentences))
    table.add_row("Paragraphs", str(stats.paragraphs))
    table.add_row("Lines", str(stats.lines))
    table.add_row("Reading Time", stats.reading_time)
    console.print(table)


@app.command(name="sort")
def sort_cmd(
    text: str | None = typer.Argument(None, help="Text to sort (or pipe via stdin)"),
    mode: str = typer.Option("alpha", "--mode", "-m", help="Sort mode"),
) -> None:
    """Sort lines (alpha, alpha-desc, length, numeric, reverse, shuffle)."""
    content = _read_input(text)
    result = engine.sort_lines(content, mode)  # type: ignore[arg-type]
    console.print(result)


@app.command()
def base64(
    direction: str = typer.Argument("encode", help="encode or decode"),
    text: str | None = typer.Argument(None, help="Text (or pipe via stdin)"),
) -> None:
    """Encode or decode Base64."""
    content = _read_input(text)
    if direction == "decode":
        result = engine.base64_decode(content)
    else:
        result = engine.base64_encode(content)
    console.print(result)


@app.command()
def url(
    direction: str = typer.Argument("encode", help="encode or decode"),
    text: str | None = typer.Argument(None, help="Text (or pipe via stdin)"),
) -> None:
    """URL encode or decode text."""
    content = _read_input(text)
    result = engine.url_decode(content) if direction == "decode" else engine.url_encode(content)
    console.print(result)


@app.command(name="html")
def html_cmd(
    direction: str = typer.Argument("encode", help="encode or decode"),
    text: str | None = typer.Argument(None, help="Text (or pipe via stdin)"),
) -> None:
    """Encode or decode HTML entities."""
    content = _read_input(text)
    result = engine.html_decode(content) if direction == "decode" else engine.html_encode(content)
    console.print(result)


@app.command()
def dedupe(
    text: str | None = typer.Argument(None, help="Text to deduplicate (or pipe via stdin)"),
    case_sensitive: bool = typer.Option(
        True, "--case-sensitive/--ignore-case", help="Case sensitivity"
    ),
) -> None:
    """Remove duplicate lines."""
    content = _read_input(text)
    result = engine.dedupe_lines(content, case_sensitive=case_sensitive)
    console.print(result)


@app.command(name="extract")
def extract_cmd(
    pattern: str = typer.Argument("emails", help="Pattern type to extract"),
    text: str | None = typer.Argument(None, help="Text to search (or pipe via stdin)"),
) -> None:
    """Extract emails, URLs, phones, numbers, IPs, hashtags, or mentions."""
    content = _read_input(text)
    results = engine.extract(content, pattern)  # type: ignore[arg-type]
    for item in results:
        console.print(item)


@app.command()
def lorem(
    count: int = typer.Argument(5, help="Number of units to generate"),
    unit: str = typer.Option("paragraphs", "--unit", "-u", help="words, sentences, or paragraphs"),
) -> None:
    """Generate Lorem Ipsum placeholder text."""
    result = engine.lorem_ipsum(count, unit)  # type: ignore[arg-type]
    console.print(result)


@app.command()
def reverse(
    text: str | None = typer.Argument(None, help="Text to reverse (or pipe via stdin)"),
    mode: str = typer.Option("characters", "--mode", "-m", help="characters, words, or lines"),
) -> None:
    """Reverse text by characters, words, or lines."""
    content = _read_input(text)
    result = engine.reverse_text(content, mode)  # type: ignore[arg-type]
    console.print(result)


@app.command(name="json")
def json_cmd(
    action: str = typer.Argument("format", help="format, minify, or validate"),
    text: str | None = typer.Argument(None, help="JSON text (or pipe via stdin)"),
) -> None:
    """Format, minify, or validate JSON."""
    content = _read_input(text)
    if action == "minify":
        console.print(engine.json_minify(content))
    elif action == "validate":
        valid = engine.json_validate(content)
        console.print("[green]Valid JSON[/green]" if valid else "[red]Invalid JSON[/red]")
    else:
        console.print(engine.json_format(content))


if __name__ == "__main__":
    app()
