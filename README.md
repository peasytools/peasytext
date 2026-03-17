# peasytext

[![PyPI version](https://agentgif.com/badge/pypi/peasytext/version.svg)](https://pypi.org/project/peasytext/)
[![Python](https://img.shields.io/pypi/pyversions/peasytext)](https://pypi.org/project/peasytext/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](https://pypi.org/project/peasytext/)

Pure Python text processing toolkit — 15 tools for case conversion, slug generation, word counting, line sorting, Base64/URL/HTML encoding, find & replace, deduplication, line numbering, pattern extraction, text diffing, Lorem Ipsum generation, JSON formatting, and text reversal. Zero dependencies.

Extracted from the client-side engines at [peasytext.com](https://peasytext.com), where all 15 text tools run entirely in the browser. This Python package provides the same functionality for server-side and CLI usage.

> **Try the interactive tools at [peasytext.com](https://peasytext.com)** — [Text Tools](https://peasytext.com/), [Text Glossary](https://peasytext.com/glossary/), [Text Formats](https://peasytext.com/formats/)

<p align="center">
  <img src="demo.gif" alt="peasytext demo — case conversion, slug generation, word counting in Python REPL" width="800">
</p>

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
- [Also Available](#also-available)
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

Learn more: [PeasyText Tools](https://peasytext.com/) · [Text Glossary](https://peasytext.com/glossary/)

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

Learn more: [PeasyText](https://peasytext.com/) · [Text Glossary](https://peasytext.com/glossary/)

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

Learn more: [PeasyText](https://peasytext.com/) · [Text Guides](https://peasytext.com/guides/)

### Line Sorting

Sort lines alphabetically, by length, numerically, or reverse order.

```python
from peasytext import sort_lines

text = "banana\napple\ncherry"
print(sort_lines(text, "alpha"))        # apple\nbanana\ncherry
print(sort_lines(text, "length"))       # apple\nbanana\ncherry
print(sort_lines("10\n2\n30", "numeric"))  # 2\n10\n30
```

Learn more: [PeasyText](https://peasytext.com/) · [Text Glossary](https://peasytext.com/glossary/)

### Base64 Encoding

Encode and decode Base64 with full UTF-8 support — handles emoji, CJK characters, and all Unicode.

```python
from peasytext import base64_encode, base64_decode

encoded = base64_encode("Hello, 世界! 🌍")
print(encoded)                    # "SGVsbG8sIOS4lueVjCEg8J+MjQ=="
print(base64_decode(encoded))     # "Hello, 世界! 🌍"
```

Learn more: [PeasyText](https://peasytext.com/) · [Base64 Glossary](https://peasytext.com/glossary/)

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

Learn more: [PeasyText](https://peasytext.com/) · [Text Glossary](https://peasytext.com/glossary/)

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

Learn more: [PeasyText](https://peasytext.com/)

### Deduplication

Remove duplicate lines while preserving original order.

```python
from peasytext import dedupe_lines

print(dedupe_lines("apple\nbanana\napple\ncherry\nbanana"))
# "apple\nbanana\ncherry"
```

Learn more: [PeasyText](https://peasytext.com/)

### Line Numbers

Add or remove line numbers from text — useful for code snippets and documentation.

```python
from peasytext import add_line_numbers, remove_line_numbers

print(add_line_numbers("first\nsecond\nthird"))
# "1: first\n2: second\n3: third"
```

Learn more: [PeasyText](https://peasytext.com/)

### Pattern Extraction

Extract emails, URLs, phone numbers, IP addresses, hashtags, and @mentions from any text.

```python
from peasytext import extract

text = "Contact info@example.com, visit https://example.com, call +1-555-0123"
print(extract(text, "emails"))   # ["info@example.com"]
print(extract(text, "urls"))     # ["https://example.com,"]
print(extract(text, "phones"))   # ["+1-555-0123"]
```

Learn more: [PeasyText](https://peasytext.com/)

### Text Diffing

Compare two texts line by line and measure similarity.

```python
from peasytext import diff_texts

result = diff_texts("apple\nbanana\ncherry", "banana\ncherry\ndate")
print(result.added)       # ["date"]
print(result.removed)     # ["apple"]
print(result.similarity)  # 0.6667
```

Learn more: [PeasyText](https://peasytext.com/)

### Lorem Ipsum

Generate placeholder text by words, sentences, or paragraphs.

```python
from peasytext import lorem_ipsum

print(lorem_ipsum(10, "words"))       # 10 lorem ipsum words
print(lorem_ipsum(3, "paragraphs"))   # 3 paragraphs of text
```

Learn more: [PeasyText](https://peasytext.com/)

### JSON Formatting

Format, minify, and validate JSON strings.

```python
from peasytext import json_format, json_minify, json_validate

print(json_format('{"a":1,"b":2}'))   # Pretty-printed JSON
print(json_minify('{ "a": 1 }'))      # {"a":1}
print(json_validate('{"key": "ok"}')) # True
```

Learn more: [PeasyText](https://peasytext.com/) · [JSON Glossary](https://peasytext.com/glossary/)

### Text Reversal

Reverse text by characters, words, or lines.

```python
from peasytext import reverse_text

print(reverse_text("hello", "characters"))      # "olleh"
print(reverse_text("hello world", "words"))     # "world hello"
print(reverse_text("a\nb\nc", "lines"))         # "c\nb\na"
```

Learn more: [PeasyText](https://peasytext.com/)

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

# Search the text processing glossary for technical terms
terms = api.search_glossary("unicode")
for term in terms:
    print(f"{term['term']}: {term['definition']}")

# Browse text processing guides and tutorials
guides = api.list_guides()
for guide in guides:
    print(f"{guide['title']}: {guide['url']}")

# Discover use cases for text operations
use_cases = api.list_use_cases()
for uc in use_cases:
    print(f"{uc['title']}: {uc['description']}")
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

- **Tools**: [Case Converter](https://peasytext.com/text/case-converter/) · [Slug Generator](https://peasytext.com/text/slug-generator/) · [Word Counter](https://peasytext.com/text/word-counter/) · [All Text Tools](https://peasytext.com/)
- **Guides**: [Text Encoding Guide](https://peasytext.com/guides/) · [Regex Guide](https://peasytext.com/guides/) · [All Guides](https://peasytext.com/guides/)
- **Glossary**: [Unicode](https://peasytext.com/glossary/unicode/) · [Base64](https://peasytext.com/glossary/) · [All Terms](https://peasytext.com/glossary/)
- **Formats**: [Plain Text](https://peasytext.com/formats/) · [JSON](https://peasytext.com/formats/json/) · [All Formats](https://peasytext.com/formats/)
- **API**: [REST API Docs](https://peasytext.com/developers/) · [OpenAPI Spec](https://peasytext.com/api/openapi.json)

## Also Available

| Platform | Install | Link |
|----------|---------|------|
| **TypeScript / npm** | `npm install peasytext` | [npm](https://www.npmjs.com/package/peasytext) |
| **Go** | `go get github.com/peasytools/peasytext-go` | [pkg.go.dev](https://pkg.go.dev/github.com/peasytools/peasytext-go) |
| **Rust** | `cargo add peasytext` | [crates.io](https://crates.io/crates/peasytext) |
| **Ruby** | `gem install peasytext` | [RubyGems](https://rubygems.org/gems/peasytext) |
| **MCP** | `uvx --from "peasytext[mcp]" python -m peasytext.mcp_server` | [Config](#mcp-server-claude-cursor-windsurf) |

## Peasy Developer Tools

Part of the [Peasy](https://peasytools.com) open-source developer tools ecosystem.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| peasy-pdf | [PyPI](https://pypi.org/project/peasy-pdf/) | [npm](https://www.npmjs.com/package/peasy-pdf) | PDF merge, split, compress, 21 operations — [peasypdf.com](https://peasypdf.com) |
| peasy-image | [PyPI](https://pypi.org/project/peasy-image/) | [npm](https://www.npmjs.com/package/peasy-image) | Image resize, crop, convert, compress, 20 operations — [peasyimage.com](https://peasyimage.com) |
| **peasytext** | **[PyPI](https://pypi.org/project/peasytext/)** | **[npm](https://www.npmjs.com/package/peasytext)** | **Text case, slugify, word count, encoding — [peasytext.com](https://peasytext.com)** |
| peasy-css | [PyPI](https://pypi.org/project/peasy-css/) | [npm](https://www.npmjs.com/package/peasy-css) | CSS gradients, shadows, flexbox, grid generators — [peasycss.com](https://peasycss.com) |
| peasy-compress | [PyPI](https://pypi.org/project/peasy-compress/) | [npm](https://www.npmjs.com/package/peasy-compress) | ZIP, TAR, gzip, brotli archive operations — [peasytools.com](https://peasytools.com) |
| peasy-document | [PyPI](https://pypi.org/project/peasy-document/) | [npm](https://www.npmjs.com/package/peasy-document) | Markdown, HTML, CSV, JSON conversions — [peasyformats.com](https://peasyformats.com) |
| peasy-audio | [PyPI](https://pypi.org/project/peasy-audio/) | [npm](https://www.npmjs.com/package/peasy-audio) | Audio convert, trim, merge, normalize — [peasyaudio.com](https://peasyaudio.com) |
| peasy-video | [PyPI](https://pypi.org/project/peasy-video/) | [npm](https://www.npmjs.com/package/peasy-video) | Video trim, resize, GIF conversion — [peasyvideo.com](https://peasyvideo.com) |

## License

MIT
