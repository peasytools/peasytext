"""peasytext — Pure Python text processing engine.

15 text operations: case conversion, slug generation, word counting,
line sorting, Base64 encode/decode, URL encode/decode, HTML entities,
find & replace, deduplication, line numbering, extraction, diffing,
Lorem Ipsum generation, and text reversal.

Zero dependencies. All functions are pure — no side effects.
"""

from __future__ import annotations

import base64
import html
import re
import unicodedata
from dataclasses import dataclass
from typing import Literal
from urllib.parse import quote, unquote

# ── Data types ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class TextStats:
    """Statistics about a text string."""

    characters: int
    characters_no_spaces: int
    words: int
    sentences: int
    paragraphs: int
    lines: int
    reading_time: str


@dataclass(frozen=True)
class DiffResult:
    """Result of comparing two texts."""

    added: list[str]
    removed: list[str]
    unchanged: list[str]
    similarity: float  # 0.0 to 1.0


# ── Case conversion ────────────────────────────────────────────────

CaseType = Literal[
    "upper",
    "lower",
    "title",
    "sentence",
    "camel",
    "pascal",
    "snake",
    "kebab",
    "constant",
    "dot",
    "path",
    "alternating",
    "inverse",
]


def to_case(text: str, target: CaseType = "upper") -> str:
    """Convert text to the specified case.

    Supports: upper, lower, title, sentence, camelCase, PascalCase,
    snake_case, kebab-case, CONSTANT_CASE, dot.case, path/case,
    aLtErNaTiNg, and iNVERSE case.
    """
    if target == "upper":
        return text.upper()
    if target == "lower":
        return text.lower()
    if target == "title":
        return re.sub(r"\w\S*", lambda m: m.group(0)[0].upper() + m.group(0)[1:].lower(), text)
    if target == "sentence":
        return re.sub(
            r"(^\s*|[.!?]\s+)([a-z])",
            lambda m: m.group(1) + m.group(2).upper(),
            text,
        )

    # Split into words for programming cases
    words = _split_words(text)
    if not words:
        return ""

    if target == "camel":
        return words[0].lower() + "".join(w.capitalize() for w in words[1:])
    if target == "pascal":
        return "".join(w.capitalize() for w in words)
    if target == "snake":
        return "_".join(w.lower() for w in words)
    if target == "kebab":
        return "-".join(w.lower() for w in words)
    if target == "constant":
        return "_".join(w.upper() for w in words)
    if target == "dot":
        return ".".join(w.lower() for w in words)
    if target == "path":
        return "/".join(w.lower() for w in words)
    if target == "alternating":
        return "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text))
    if target == "inverse":
        return text.swapcase()
    return text


def _split_words(text: str) -> list[str]:
    """Split text into words, handling camelCase, snake_case, etc."""
    # Insert space before uppercase letters in camelCase
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    # Split on non-alphanumeric characters
    return [w for w in re.split(r"[^a-zA-Z0-9]+", s) if w]


# ── Slug generation ─────────────────────────────────────────────────


def slugify(
    text: str,
    *,
    separator: str = "-",
    lowercase: bool = True,
    max_length: int = 0,
) -> str:
    """Convert text to a URL-friendly slug.

    Strips diacritics, replaces non-alphanumeric characters with the separator,
    and optionally truncates to max_length without breaking mid-word.
    """
    lines = text.split("\n")
    results: list[str] = []

    for line in lines:
        line = line.strip()
        if not line:
            results.append("")
            continue

        # Normalize unicode — strip diacritics
        slug = unicodedata.normalize("NFD", line)
        slug = re.sub(r"[\u0300-\u036f]", "", slug)

        if lowercase:
            slug = slug.lower()

        # Replace non-alphanumeric with separator
        slug = re.sub(r"[^a-zA-Z0-9]+", separator, slug)

        # Trim separators from edges
        slug = slug.strip(separator)

        # Apply max length
        if max_length > 0 and len(slug) > max_length:
            slug = slug[:max_length].rstrip(separator)

        results.append(slug)

    return "\n".join(results)


# ── Text statistics ─────────────────────────────────────────────────


def count_text(text: str, *, words_per_minute: int = 200) -> TextStats:
    """Count characters, words, sentences, paragraphs, and lines.

    Also estimates reading time based on the given words-per-minute rate.
    """
    chars = len(text)
    chars_no_spaces = len(
        text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
    )

    # Words
    words = len(text.split()) if text.strip() else 0

    # Sentences
    sentences = len([s for s in re.split(r"[.!?]+\s*", text) if s.strip()]) if text.strip() else 0

    # Paragraphs
    paragraphs = len([p for p in re.split(r"\n\s*\n", text) if p.strip()]) if text.strip() else 0

    # Lines
    lines = len(text.split("\n")) if text else 0

    # Reading time
    reading_minutes = words / words_per_minute if words_per_minute > 0 else 0
    if reading_minutes < 1:
        reading_time = "< 1 min"
    else:
        import math

        reading_time = f"{math.ceil(reading_minutes)} min"

    return TextStats(
        characters=chars,
        characters_no_spaces=chars_no_spaces,
        words=words,
        sentences=sentences,
        paragraphs=paragraphs,
        lines=lines,
        reading_time=reading_time,
    )


# ── Sort lines ──────────────────────────────────────────────────────

SortMode = Literal[
    "alpha",
    "alpha-desc",
    "length",
    "length-desc",
    "numeric",
    "reverse",
    "random",
    "shuffle",
]


def sort_lines(text: str, mode: SortMode = "alpha") -> str:
    """Sort lines of text by various criteria."""
    lines = text.split("\n")

    if mode == "alpha":
        lines.sort(key=str.lower)
    elif mode == "alpha-desc":
        lines.sort(key=str.lower, reverse=True)
    elif mode == "length":
        lines.sort(key=len)
    elif mode == "length-desc":
        lines.sort(key=len, reverse=True)
    elif mode == "numeric":
        lines.sort(key=_numeric_key)
    elif mode in ("reverse",):
        lines.reverse()
    elif mode in ("random", "shuffle"):
        import random

        random.shuffle(lines)

    return "\n".join(lines)


def _numeric_key(line: str) -> float:
    """Extract leading number for numeric sorting."""
    match = re.match(r"[\s]*(-?[\d,]*\.?\d+)", line)
    if match:
        return float(match.group(1).replace(",", ""))
    return float("inf")


# ── Base64 encode/decode ────────────────────────────────────────────


def base64_encode(text: str) -> str:
    """Encode text to Base64 (UTF-8 safe)."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def base64_decode(text: str) -> str:
    """Decode Base64 to text (UTF-8 safe).

    Raises ValueError if the input is not valid Base64.
    """
    try:
        return base64.b64decode(text.strip()).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Invalid Base64 input: {e}") from e


# ── URL encode/decode ───────────────────────────────────────────────


def url_encode(text: str, *, plus: bool = False) -> str:
    """URL-encode text. If plus=True, spaces become + instead of %20."""
    if plus:
        from urllib.parse import quote_plus

        return quote_plus(text)
    return quote(text, safe="")


def url_decode(text: str) -> str:
    """URL-decode text."""
    return unquote(text)


# ── HTML entities ───────────────────────────────────────────────────


def html_encode(text: str) -> str:
    """Encode special characters as HTML entities."""
    return html.escape(text, quote=True)


def html_decode(text: str) -> str:
    """Decode HTML entities back to characters."""
    return html.unescape(text)


# ── Find & replace ──────────────────────────────────────────────────


def find_replace(
    text: str,
    find: str,
    replace: str = "",
    *,
    case_sensitive: bool = True,
    regex: bool = False,
) -> str:
    """Find and replace text. Supports plain text and regex patterns."""
    if not find:
        return text

    if regex:
        flags = 0 if case_sensitive else re.IGNORECASE
        return re.sub(find, replace, text, flags=flags)

    if case_sensitive:
        return text.replace(find, replace)

    # Case-insensitive plain text replacement
    pattern = re.escape(find)
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)


# ── Deduplicate lines ──────────────────────────────────────────────


def dedupe_lines(text: str, *, case_sensitive: bool = True) -> str:
    """Remove duplicate lines, preserving order."""
    seen: set[str] = set()
    result: list[str] = []

    for line in text.split("\n"):
        key = line if case_sensitive else line.lower()
        if key not in seen:
            seen.add(key)
            result.append(line)

    return "\n".join(result)


# ── Line numbers ────────────────────────────────────────────────────


def add_line_numbers(
    text: str,
    *,
    start: int = 1,
    separator: str = ": ",
    padding: bool = True,
) -> str:
    """Add line numbers to each line of text."""
    lines = text.split("\n")
    end = start + len(lines) - 1
    width = len(str(end)) if padding else 0

    result: list[str] = []
    for i, line in enumerate(lines, start=start):
        num = str(i).rjust(width) if padding else str(i)
        result.append(f"{num}{separator}{line}")

    return "\n".join(result)


def remove_line_numbers(text: str) -> str:
    """Remove leading line numbers from text."""
    return re.sub(r"^\s*\d+[.:\-)\]|]\s?", "", text, flags=re.MULTILINE)


# ── Extract patterns ───────────────────────────────────────────────

ExtractType = Literal["emails", "urls", "phones", "numbers", "ips", "hashtags", "mentions"]


def extract(text: str, pattern_type: ExtractType = "emails") -> list[str]:
    """Extract emails, URLs, phone numbers, or other patterns from text."""
    patterns: dict[str, str] = {
        "emails": r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
        "urls": r"https?://[^\s<>\"']+",
        "phones": r"(?:\+?\d{1,3}[\s.-]?)?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}",
        "numbers": r"-?\d+(?:,\d{3})*(?:\.\d+)?",
        "ips": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        "hashtags": r"#\w+",
        "mentions": r"@\w+",
    }
    regex = patterns.get(pattern_type, patterns["emails"])
    return re.findall(regex, text)


# ── Diff two texts ──────────────────────────────────────────────────


def diff_texts(text_a: str, text_b: str) -> DiffResult:
    """Compare two texts line by line."""
    lines_a = set(text_a.split("\n"))
    lines_b = set(text_b.split("\n"))

    added = sorted(lines_b - lines_a)
    removed = sorted(lines_a - lines_b)
    unchanged = sorted(lines_a & lines_b)

    total = len(lines_a | lines_b)
    similarity = len(unchanged) / total if total > 0 else 1.0

    return DiffResult(
        added=added,
        removed=removed,
        unchanged=unchanged,
        similarity=round(similarity, 4),
    )


# ── Lorem Ipsum generator ──────────────────────────────────────────

_LOREM_WORDS = [
    "lorem",
    "ipsum",
    "dolor",
    "sit",
    "amet",
    "consectetur",
    "adipiscing",
    "elit",
    "sed",
    "do",
    "eiusmod",
    "tempor",
    "incididunt",
    "ut",
    "labore",
    "et",
    "dolore",
    "magna",
    "aliqua",
    "enim",
    "ad",
    "minim",
    "veniam",
    "quis",
    "nostrud",
    "exercitation",
    "ullamco",
    "laboris",
    "nisi",
    "aliquip",
    "ex",
    "ea",
    "commodo",
    "consequat",
    "duis",
    "aute",
    "irure",
    "in",
    "reprehenderit",
    "voluptate",
    "velit",
    "esse",
    "cillum",
    "fugiat",
    "nulla",
    "pariatur",
    "excepteur",
    "sint",
    "occaecat",
    "cupidatat",
    "non",
    "proident",
    "sunt",
    "culpa",
    "qui",
    "officia",
    "deserunt",
    "mollit",
    "anim",
    "id",
    "est",
    "laborum",
]

LoremUnit = Literal["words", "sentences", "paragraphs"]


def lorem_ipsum(count: int = 5, unit: LoremUnit = "paragraphs") -> str:
    """Generate Lorem Ipsum placeholder text.

    Args:
        count: Number of words, sentences, or paragraphs.
        unit: "words", "sentences", or "paragraphs".
    """
    if count <= 0:
        return ""

    if unit == "words":
        words: list[str] = []
        while len(words) < count:
            words.extend(_LOREM_WORDS)
        return " ".join(words[:count])

    if unit == "sentences":
        sentences: list[str] = []
        word_pool = list(_LOREM_WORDS)
        idx = 0
        for _ in range(count):
            length = 8 + (idx % 7)  # 8-14 words per sentence
            words_in_sentence: list[str] = []
            for _ in range(length):
                words_in_sentence.append(word_pool[idx % len(word_pool)])
                idx += 1
            sent = " ".join(words_in_sentence)
            sentences.append(sent[0].upper() + sent[1:] + ".")
        return " ".join(sentences)

    # paragraphs
    paragraphs: list[str] = []
    for i in range(count):
        # 3-6 sentences per paragraph
        num_sentences = 3 + (i % 4)
        para = lorem_ipsum(num_sentences, "sentences")
        paragraphs.append(para)
    return "\n\n".join(paragraphs)


# ── Reverse text ────────────────────────────────────────────────────

ReverseMode = Literal["characters", "words", "lines"]


def reverse_text(text: str, mode: ReverseMode = "characters") -> str:
    """Reverse text by characters, words, or lines."""
    if mode == "characters":
        return text[::-1]
    if mode == "words":
        return " ".join(text.split()[::-1])
    if mode == "lines":
        return "\n".join(text.split("\n")[::-1])
    return text


# ── JSON format/validate ───────────────────────────────────────────


def json_format(text: str, *, indent: int = 2) -> str:
    """Format (pretty-print) a JSON string.

    Raises ValueError if the input is not valid JSON.
    """
    import json

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e
    return json.dumps(data, indent=indent, ensure_ascii=False)


def json_minify(text: str) -> str:
    """Minify a JSON string by removing all whitespace.

    Raises ValueError if the input is not valid JSON.
    """
    import json

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


def json_validate(text: str) -> bool:
    """Check if a string is valid JSON."""
    import json

    try:
        json.loads(text)
        return True
    except (json.JSONDecodeError, ValueError):
        return False
