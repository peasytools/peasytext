# peasytext

[![PyPI](https://img.shields.io/pypi/v/peasytext)](https://pypi.org/project/peasytext/)
[![Python](https://img.shields.io/pypi/pyversions/peasytext)](https://pypi.org/project/peasytext/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](https://pypi.org/project/peasytext/)

Pure Python text processing toolkit — 15 tools for case conversion, slug generation, word counting, line sorting, Base64/URL/HTML encoding, find & replace, deduplication, line numbering, pattern extraction, text diffing, Lorem Ipsum generation, JSON formatting, and text reversal. Zero dependencies.

Extracted from the client-side engines at [peasytext.com](https://peasytext.com), where all 15 text tools run entirely in the browser. This Python package provides the same functionality for server-side and CLI usage.

> **Try the interactive tools at [peasytext.com](https://peasytext.com)** — [Text Case Converter](https://peasytext.com/tools/text-case-converter/), [Word Counter](https://peasytext.com/tools/word-counter/), [Slug Generator](https://peasytext.com/tools/slug-generator/), [Base64 Encoder](https://peasytext.com/tools/base64-encoder-decoder/), [JSON Formatter](https://peasytext.com/tools/json-formatter/)

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [What You Can Do](#what-you-can-do)
  - [Case Conversion](#case-conversion)
  - [Slug Generation](#slug-generation)
  - [Text Statistics](#text-statistics)
  - [Line Sorting](#line-sorting)
  - [Base64 Encoding](#base64-encoding)
  - [URL & HTML Encoding](#url--html-encoding)
  - [Find & Replace](#find--replace)
  - [Deduplication](#deduplication)
  - [Line Numbers](#line-numbers)
  - [Pattern Extraction](#pattern-extraction)
  - [Text Diffing](#text-diffing)
  - [Lorem Ipsum](#lorem-ipsum)
  - [JSON Formatting](#json-formatting)
  - [Text Reversal](#text-reversal)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [API Reference](#api-reference)
- [Learn More About Text Processing](#learn-more-about-text-processing)
- [Peasy Developer Tools](#peasy-developer-tools)
- [License](#license)

## Install

```bash
pip install peasytext              # Core (zero dependencies)
pip install "peasytext[cli]"       # + CLI (typer, rich)
pip install "peasytext[mcp]"       # + MCP server
pip install "peasytext[api]"       # + REST API client (httpx)
pip install "peasytext[all]"       # Everything
```

## Quick Start

```python
from peasytext import to_case, slugify, count_text, extract

# Convert text between 13 case formats
print(to_case("hello world", "pascal"))     # "HelloWorld"
print(to_case("hello world", "snake"))      # "hello_world"
print(to_case("hello world", "constant"))   # "HELLO_WORLD"

# Generate URL-friendly slugs
print(slugify("Crème brûlée recipe!"))      # "creme-brulee-recipe"

# Count words, sentences, reading time
stats = count_text("Hello world. How are you today?")
print(stats.words)          # 6
print(stats.sentences)      # 2
print(stats.reading_time)   # "< 1 min"

# Extract patterns from text
emails = extract("Contact info@example.com or admin@test.org", "emails")
print(emails)  # ["info@example.com", "admin@test.org"]
```

## What You Can Do

### Case Conversion

Convert text between 13 case formats — from basic upper/lower to programming conventions like camelCase, snake_case, and CONSTANT_CASE.

| Case | Example | Use Case |
|------|---------|----------|
| `upper` | HELLO WORLD | Constants, emphasis |
| `lower` | hello world | Normalization |
| `title` | Hello World | Headings, titles |
| `sentence` | Hello world | Natural text |
| `camel` | helloWorld | JavaScript variables |
| `pascal` | HelloWorld | Class names |
| `snake` | hello_world | Python variables |
| `kebab` | hello-world | CSS classes, URLs |
| `constant` | HELLO_WORLD | Constants, env vars |
| `dot` | hello.world | Package names |
| `path` | hello/world | File paths |
| `alternating` | hElLo WoRlD | Sarcasm text |
| `inverse` | hELLO wORLD | Inversion |

```python
from peasytext import to_case

# Programming case conversions
print(to_case("user full name", "camel"))     # "userFullName"
print(to_case("user full name", "pascal"))    # "UserFullName"
print(to_case("user full name", "snake"))     # "user_full_name"
print(to_case("user full name", "constant"))  # "USER_FULL_NAME"
```

### Slug Generation

Convert any text to a URL-friendly slug. Handles Unicode, diacritics, and special characters. Essential for SEO-friendly URLs, file naming, and database keys.

```python
from peasytext import slugify

# Basic slugification with diacritic handling
print(slugify("Crème Brûlée — The Recipe"))  # "creme-brulee-the-recipe"
print(slugify("München Straße"))               # "munchen-strasse"

# Custom separator and length limit
print(slugify("Hello World", separator="_"))           # "hello_world"
print(slugify("A very long title here", max_length=10))  # "a-very"
```

### Text Statistics

Count characters, words, sentences, paragraphs, and lines. Also estimates reading time — useful for blog posts, content management, and SEO metadata.

```python
from peasytext import count_text

stats = count_text("Hello world. This is a test.\n\nNew paragraph here.")
print(f"Words: {stats.words}")                # 9
print(f"Sentences: {stats.sentences}")        # 3
print(f"Paragraphs: {stats.paragraphs}")      # 2
print(f"Reading time: {stats.reading_time}")   # "< 1 min"
```

### Line Sorting

Sort lines alphabetically, by length, numerically, or reverse order.

```python
from peasytext import sort_lines

text = "banana\napple\ncherry"
print(sort_lines(text, "alpha"))        # apple\nbanana\ncherry
print(sort_lines(text, "length"))       # apple\nbanana\ncherry
print(sort_lines("10\n2\n30", "numeric"))  # 2\n10\n30
```

### Base64 Encoding

Encode and decode Base64 with full UTF-8 support — handles emoji, CJK characters, and all Unicode.

```python
from peasytext import base64_encode, base64_decode

encoded = base64_encode("Hello, 世界! 🌍")
print(encoded)                    # "SGVsbG8sIOS4lueVjCEg8J+MjQ=="
print(base64_decode(encoded))     # "Hello, 世界! 🌍"
```

### URL & HTML Encoding

```python
from peasytext import url_encode, url_decode, html_encode, html_decode

# URL encoding
print(url_encode("hello world"))   # "hello%20world"
print(url_decode("hello%20world")) # "hello world"

# HTML entity encoding — prevent XSS
print(html_encode('<script>alert("xss")</script>'))
# "&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;"
```

### Find & Replace

Plain text and regex find & replace with case sensitivity options.

```python
from peasytext import find_replace

print(find_replace("Hello World", "world", "Python", case_sensitive=False))
# "Hello Python"

# Regex mode — replace all numbers
print(find_replace("abc123def456", r"\d+", "NUM", regex=True))
# "abcNUMdefNUM"
```

### Deduplication

Remove duplicate lines while preserving original order.

```python
from peasytext import dedupe_lines

print(dedupe_lines("apple\nbanana\napple\ncherry\nbanana"))
# "apple\nbanana\ncherry"
```

### Line Numbers

Add or remove line numbers from text — useful for code snippets and documentation.

```python
from peasytext import add_line_numbers, remove_line_numbers

print(add_line_numbers("first\nsecond\nthird"))
# "1: first\n2: second\n3: third"
```

### Pattern Extraction

Extract emails, URLs, phone numbers, IP addresses, hashtags, and @mentions from any text.

```python
from peasytext import extract

text = "Contact info@example.com, visit https://example.com, call +1-555-0123"
print(extract(text, "emails"))   # ["info@example.com"]
print(extract(text, "urls"))     # ["https://example.com,"]
print(extract(text, "phones"))   # ["+1-555-0123"]
```

### Text Diffing

Compare two texts line by line and measure similarity.

```python
from peasytext import diff_texts

result = diff_texts("apple\nbanana\ncherry", "banana\ncherry\ndate")
print(result.added)       # ["date"]
print(result.removed)     # ["apple"]
print(result.similarity)  # 0.6667
```

### Lorem Ipsum

Generate placeholder text by words, sentences, or paragraphs.

```python
from peasytext import lorem_ipsum

print(lorem_ipsum(10, "words"))       # 10 lorem ipsum words
print(lorem_ipsum(3, "paragraphs"))   # 3 paragraphs of text
```

### JSON Formatting

Format, minify, and validate JSON strings.

```python
from peasytext import json_format, json_minify, json_validate

print(json_format('{"a":1,"b":2}'))   # Pretty-printed JSON
print(json_minify('{ "a": 1 }'))      # {"a":1}
print(json_validate('{"key": "ok"}')) # True
```

### Text Reversal

Reverse text by characters, words, or lines.

```python
from peasytext import reverse_text

print(reverse_text("hello", "characters"))      # "olleh"
print(reverse_text("hello world", "words"))     # "world hello"
print(reverse_text("a\nb\nc", "lines"))         # "c\nb\na"
```

## Command-Line Interface

```bash
pip install "peasytext[cli]"

# Case conversion
peasytext case "hello world" --target pascal   # HelloWorld

# Slug generation
peasytext slug "Hello World!"                  # hello-world

# Word counter
peasytext count "Hello world. How are you?"

# Sort lines (pipe from stdin)
echo -e "banana\napple\ncherry" | peasytext sort

# Base64 encode/decode
peasytext base64 encode "Hello"                # SGVsbG8=
peasytext base64 decode "SGVsbG8="             # Hello

# Extract patterns
echo "Email me at test@example.com" | peasytext extract emails

# Generate Lorem Ipsum
peasytext lorem 3 --unit paragraphs

# JSON formatting
echo '{"a":1}' | peasytext json format
```

## MCP Server (Claude, Cursor, Windsurf)

```bash
pip install "peasytext[mcp]"

# Run the MCP server
uvx --from "peasytext[mcp]" python -m peasytext.mcp_server
```

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
    "mcpServers": {
        "peasytext": {
            "command": "uvx",
            "args": ["--from", "peasytext[mcp]", "python", "-m", "peasytext.mcp_server"]
        }
    }
}
```

15 MCP tools available: `text_case`, `text_slug`, `text_count`, `text_sort`, `text_base64`, `text_url_encode`, `text_html_entities`, `text_find_replace`, `text_dedupe`, `text_line_numbers`, `text_extract`, `text_lorem`, `text_reverse`, `text_json`, `text_diff`.

## REST API Client

```bash
pip install "peasytext[api]"
```

```python
from peasytext.api import PeasyTextAPI

api = PeasyTextAPI()
tools = api.list_tools()
glossary = api.search("encoding")
spec = api.openapi_spec()
```

## API Reference

| Function | Description |
|----------|-------------|
| `to_case(text, target)` | Convert between 13 case formats |
| `slugify(text, **opts)` | Generate URL-friendly slug |
| `count_text(text, **opts)` | Count words, chars, sentences, reading time |
| `sort_lines(text, mode)` | Sort lines by alpha, length, numeric, etc. |
| `base64_encode(text)` | Encode text to Base64 |
| `base64_decode(text)` | Decode Base64 to text |
| `url_encode(text, **opts)` | URL-encode text |
| `url_decode(text)` | URL-decode text |
| `html_encode(text)` | Encode HTML entities |
| `html_decode(text)` | Decode HTML entities |
| `find_replace(text, find, replace, **opts)` | Find and replace with regex support |
| `dedupe_lines(text, **opts)` | Remove duplicate lines |
| `add_line_numbers(text, **opts)` | Add line numbers |
| `remove_line_numbers(text)` | Remove line numbers |
| `extract(text, pattern_type)` | Extract emails, URLs, phones, etc. |
| `diff_texts(text_a, text_b)` | Compare two texts |
| `lorem_ipsum(count, unit)` | Generate Lorem Ipsum |
| `reverse_text(text, mode)` | Reverse by chars, words, or lines |
| `json_format(text, **opts)` | Pretty-print JSON |
| `json_minify(text)` | Minify JSON |
| `json_validate(text)` | Validate JSON |

## Learn More About Text Processing

- **Tools**: [Text Case Converter](https://peasytext.com/tools/text-case-converter/) · [Word Counter](https://peasytext.com/tools/word-counter/) · [Slug Generator](https://peasytext.com/tools/slug-generator/) · [Base64 Encoder](https://peasytext.com/tools/base64-encoder-decoder/)
- **Guides**: [Text Processing Guide](https://peasytext.com/guides/) · [Glossary](https://peasytext.com/glossary/)
- **Hub**: [Peasy Tools](https://peasytools.com) — 255 free browser-based tools across 16 categories

## Peasy Developer Tools

| Package | PyPI | Description |
|---------|------|-------------|
| **peasytext** | [PyPI](https://pypi.org/project/peasytext/) | **Text processing toolkit — 15 tools** — [peasytext.com](https://peasytext.com) |

More packages coming soon for all 15 Peasy categories (PDF, Image, Dev, CSS, SEO, Math, and more).

## License

MIT — see [LICENSE](LICENSE).
