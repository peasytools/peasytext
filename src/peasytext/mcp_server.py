"""peasytext MCP server — Expose text tools to AI assistants.

Run::

    uvx --from "peasytext[mcp]" python -m peasytext.mcp_server

Configure in Claude Desktop / Cursor / Windsurf::

    {
        "mcpServers": {
            "peasytext": {
                "command": "uvx",
                "args": ["--from", "peasytext[mcp]", "python", "-m", "peasytext.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from peasytext import engine

mcp = FastMCP("peasytext")


@mcp.tool()
def text_case(text: str, target: str = "upper") -> str:
    """Convert text between cases.

    target: upper, lower, title, sentence, camel, pascal, snake, kebab,
            constant, dot, path, alternating, inverse
    """
    return engine.to_case(text, target)  # type: ignore[arg-type]


@mcp.tool()
def text_slug(text: str, separator: str = "-", max_length: int = 0) -> str:
    """Convert text to a URL-friendly slug."""
    return engine.slugify(text, separator=separator, max_length=max_length)


@mcp.tool()
def text_count(text: str) -> dict[str, object]:
    """Count characters, words, sentences, paragraphs, lines, and reading time."""
    stats = engine.count_text(text)
    return {
        "characters": stats.characters,
        "characters_no_spaces": stats.characters_no_spaces,
        "words": stats.words,
        "sentences": stats.sentences,
        "paragraphs": stats.paragraphs,
        "lines": stats.lines,
        "reading_time": stats.reading_time,
    }


@mcp.tool()
def text_sort(text: str, mode: str = "alpha") -> str:
    """Sort lines (alpha, alpha-desc, length, length-desc, numeric, reverse, shuffle)."""
    return engine.sort_lines(text, mode)  # type: ignore[arg-type]


@mcp.tool()
def text_base64(text: str, direction: str = "encode") -> str:
    """Base64 encode or decode text."""
    if direction == "decode":
        return engine.base64_decode(text)
    return engine.base64_encode(text)


@mcp.tool()
def text_url_encode(text: str, direction: str = "encode") -> str:
    """URL encode or decode text."""
    if direction == "decode":
        return engine.url_decode(text)
    return engine.url_encode(text)


@mcp.tool()
def text_html_entities(text: str, direction: str = "encode") -> str:
    """Encode or decode HTML entities."""
    if direction == "decode":
        return engine.html_decode(text)
    return engine.html_encode(text)


@mcp.tool()
def text_find_replace(
    text: str, find: str, replace: str = "", case_sensitive: bool = True, regex: bool = False
) -> str:
    """Find and replace text. Supports regex."""
    return engine.find_replace(text, find, replace, case_sensitive=case_sensitive, regex=regex)


@mcp.tool()
def text_dedupe(text: str, case_sensitive: bool = True) -> str:
    """Remove duplicate lines, preserving order."""
    return engine.dedupe_lines(text, case_sensitive=case_sensitive)


@mcp.tool()
def text_line_numbers(text: str, action: str = "add", start: int = 1) -> str:
    """Add or remove line numbers."""
    if action == "remove":
        return engine.remove_line_numbers(text)
    return engine.add_line_numbers(text, start=start)


@mcp.tool()
def text_extract(text: str, pattern: str = "emails") -> list[str]:
    """Extract emails, URLs, phones, numbers, IPs, hashtags, or mentions from text."""
    return engine.extract(text, pattern)  # type: ignore[arg-type]


@mcp.tool()
def text_lorem(count: int = 5, unit: str = "paragraphs") -> str:
    """Generate Lorem Ipsum placeholder text."""
    return engine.lorem_ipsum(count, unit)  # type: ignore[arg-type]


@mcp.tool()
def text_reverse(text: str, mode: str = "characters") -> str:
    """Reverse text by characters, words, or lines."""
    return engine.reverse_text(text, mode)  # type: ignore[arg-type]


@mcp.tool()
def text_json(text: str, action: str = "format") -> str:
    """Format, minify, or validate JSON."""
    if action == "minify":
        return engine.json_minify(text)
    if action == "validate":
        return "valid" if engine.json_validate(text) else "invalid"
    return engine.json_format(text)


@mcp.tool()
def text_diff(text_a: str, text_b: str) -> dict[str, object]:
    """Compare two texts line by line."""
    result = engine.diff_texts(text_a, text_b)
    return {
        "added": result.added,
        "removed": result.removed,
        "unchanged": result.unchanged,
        "similarity": result.similarity,
    }


if __name__ == "__main__":
    mcp.run()
