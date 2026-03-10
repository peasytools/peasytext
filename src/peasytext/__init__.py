"""peasytext — Pure Python text processing toolkit.

15 text operations for case conversion, slug generation, word counting,
line sorting, Base64 encode/decode, URL encode/decode, HTML entities,
find & replace, deduplication, line numbering, pattern extraction,
text diffing, Lorem Ipsum generation, JSON formatting, and text reversal.

Zero dependencies. All functions are pure.

Usage::

    from peasytext import to_case, slugify, count_text

    print(to_case("hello world", "pascal"))   # "HelloWorld"
    print(slugify("Hello World!"))            # "hello-world"

    stats = count_text("Hello world. How are you?")
    print(stats.words)         # 5
    print(stats.sentences)     # 2
    print(stats.reading_time)  # "< 1 min"
"""

from peasytext.engine import (
    CaseType,
    DiffResult,
    ExtractType,
    LoremUnit,
    ReverseMode,
    SortMode,
    TextStats,
    add_line_numbers,
    base64_decode,
    base64_encode,
    count_text,
    dedupe_lines,
    diff_texts,
    extract,
    find_replace,
    html_decode,
    html_encode,
    json_format,
    json_minify,
    json_validate,
    lorem_ipsum,
    remove_line_numbers,
    reverse_text,
    slugify,
    sort_lines,
    to_case,
    url_decode,
    url_encode,
)

__version__ = "0.1.0"

__all__ = [
    "CaseType",
    "DiffResult",
    "ExtractType",
    "LoremUnit",
    "ReverseMode",
    "SortMode",
    "TextStats",
    "add_line_numbers",
    "base64_decode",
    "base64_encode",
    "count_text",
    "dedupe_lines",
    "diff_texts",
    "extract",
    "find_replace",
    "html_decode",
    "html_encode",
    "json_format",
    "json_minify",
    "json_validate",
    "lorem_ipsum",
    "remove_line_numbers",
    "reverse_text",
    "slugify",
    "sort_lines",
    "to_case",
    "url_decode",
    "url_encode",
]
