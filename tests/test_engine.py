"""Tests for peasytext engine — all 15 text processing functions."""

from __future__ import annotations

import pytest

from peasytext import (
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

# ── Case conversion ────────────────────────────────────────────────


class TestToCase:
    def test_upper(self) -> None:
        assert to_case("hello world", "upper") == "HELLO WORLD"

    def test_lower(self) -> None:
        assert to_case("HELLO WORLD", "lower") == "hello world"

    def test_title(self) -> None:
        assert to_case("hello world", "title") == "Hello World"

    def test_sentence(self) -> None:
        result = to_case("hello world. goodbye world.", "sentence")
        assert result.startswith("Hello")

    def test_camel(self) -> None:
        assert to_case("hello world", "camel") == "helloWorld"

    def test_pascal(self) -> None:
        assert to_case("hello world", "pascal") == "HelloWorld"

    def test_snake(self) -> None:
        assert to_case("Hello World", "snake") == "hello_world"

    def test_kebab(self) -> None:
        assert to_case("Hello World", "kebab") == "hello-world"

    def test_constant(self) -> None:
        assert to_case("hello world", "constant") == "HELLO_WORLD"

    def test_dot(self) -> None:
        assert to_case("hello world", "dot") == "hello.world"

    def test_path(self) -> None:
        assert to_case("hello world", "path") == "hello/world"

    def test_alternating(self) -> None:
        result = to_case("hello", "alternating")
        assert result == "hElLo"

    def test_inverse(self) -> None:
        assert to_case("Hello World", "inverse") == "hELLO wORLD"

    def test_camel_from_snake(self) -> None:
        assert to_case("hello_world_test", "camel") == "helloWorldTest"

    def test_empty(self) -> None:
        assert to_case("", "upper") == ""


# ── Slug ────────────────────────────────────────────────────────────


class TestSlugify:
    def test_basic(self) -> None:
        assert slugify("Hello World!") == "hello-world"

    def test_diacritics(self) -> None:
        assert slugify("Crème brûlée") == "creme-brulee"

    def test_custom_separator(self) -> None:
        assert slugify("Hello World", separator="_") == "hello_world"

    def test_no_lowercase(self) -> None:
        assert slugify("Hello World", lowercase=False) == "Hello-World"

    def test_max_length(self) -> None:
        result = slugify("this is a very long title", max_length=10)
        assert len(result) <= 10

    def test_multiline(self) -> None:
        result = slugify("Line One\nLine Two")
        assert result == "line-one\nline-two"

    def test_empty_line(self) -> None:
        result = slugify("Hello\n\nWorld")
        assert result == "hello\n\nworld"


# ── Text stats ──────────────────────────────────────────────────────


class TestCountText:
    def test_basic(self) -> None:
        stats = count_text("Hello world.")
        assert stats.words == 2
        assert stats.characters == 12
        assert stats.sentences == 1

    def test_reading_time_short(self) -> None:
        stats = count_text("Hello world")
        assert stats.reading_time == "< 1 min"

    def test_reading_time_long(self) -> None:
        text = " ".join(["word"] * 400)
        stats = count_text(text)
        assert stats.reading_time == "2 min"

    def test_paragraphs(self) -> None:
        stats = count_text("Para one.\n\nPara two.")
        assert stats.paragraphs == 2

    def test_empty(self) -> None:
        stats = count_text("")
        assert stats.words == 0
        assert stats.lines == 0

    def test_returns_textstats(self) -> None:
        stats = count_text("hello")
        assert isinstance(stats, TextStats)


# ── Sort lines ──────────────────────────────────────────────────────


class TestSortLines:
    def test_alpha(self) -> None:
        assert sort_lines("banana\napple\ncherry") == "apple\nbanana\ncherry"

    def test_alpha_desc(self) -> None:
        assert sort_lines("banana\napple\ncherry", "alpha-desc") == "cherry\nbanana\napple"

    def test_length(self) -> None:
        assert sort_lines("bb\naaa\nc", "length") == "c\nbb\naaa"

    def test_numeric(self) -> None:
        assert sort_lines("10\n2\n30", "numeric") == "2\n10\n30"

    def test_reverse(self) -> None:
        assert sort_lines("a\nb\nc", "reverse") == "c\nb\na"


# ── Base64 ──────────────────────────────────────────────────────────


class TestBase64:
    def test_encode(self) -> None:
        assert base64_encode("Hello") == "SGVsbG8="

    def test_decode(self) -> None:
        assert base64_decode("SGVsbG8=") == "Hello"

    def test_roundtrip(self) -> None:
        text = "Hello, 世界! 🌍"
        assert base64_decode(base64_encode(text)) == text

    def test_decode_invalid(self) -> None:
        with pytest.raises(ValueError, match="Invalid Base64"):
            base64_decode("not-valid-base64!!!")


# ── URL encode/decode ──────────────────────────────────────────────


class TestURLEncode:
    def test_encode(self) -> None:
        assert url_encode("hello world") == "hello%20world"

    def test_encode_plus(self) -> None:
        assert url_encode("hello world", plus=True) == "hello+world"

    def test_decode(self) -> None:
        assert url_decode("hello%20world") == "hello world"

    def test_roundtrip(self) -> None:
        text = "a=1&b=hello world"
        assert url_decode(url_encode(text)) == text


# ── HTML entities ──────────────────────────────────────────────────


class TestHTMLEntities:
    def test_encode(self) -> None:
        result = html_encode('<script>alert("xss")</script>')
        assert result == "&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;"

    def test_decode(self) -> None:
        assert html_decode("&lt;b&gt;bold&lt;/b&gt;") == "<b>bold</b>"

    def test_roundtrip(self) -> None:
        text = '<a href="test">link & text</a>'
        assert html_decode(html_encode(text)) == text


# ── Find & replace ─────────────────────────────────────────────────


class TestFindReplace:
    def test_basic(self) -> None:
        assert find_replace("hello world", "world", "Python") == "hello Python"

    def test_case_insensitive(self) -> None:
        assert find_replace("Hello World", "hello", "hi", case_sensitive=False) == "hi World"

    def test_regex(self) -> None:
        assert find_replace("abc123def456", r"\d+", "NUM", regex=True) == "abcNUMdefNUM"

    def test_empty_find(self) -> None:
        assert find_replace("hello", "", "x") == "hello"


# ── Dedupe ─────────────────────────────────────────────────────────


class TestDedupeLines:
    def test_basic(self) -> None:
        assert dedupe_lines("a\nb\na\nc\nb") == "a\nb\nc"

    def test_case_insensitive(self) -> None:
        assert dedupe_lines("Hello\nhello\nHELLO", case_sensitive=False) == "Hello"

    def test_preserves_order(self) -> None:
        assert dedupe_lines("c\na\nb\na") == "c\na\nb"


# ── Line numbers ───────────────────────────────────────────────────


class TestLineNumbers:
    def test_add(self) -> None:
        result = add_line_numbers("a\nb\nc")
        assert result == "1: a\n2: b\n3: c"

    def test_add_custom_start(self) -> None:
        result = add_line_numbers("a\nb", start=10)
        assert result.startswith("10: a")

    def test_remove(self) -> None:
        assert remove_line_numbers("1: a\n2: b\n3: c") == "a\nb\nc"


# ── Extract ─────────────────────────────────────────────────────────


class TestExtract:
    def test_emails(self) -> None:
        text = "Contact us at info@example.com or admin@test.org"
        result = extract(text, "emails")
        assert "info@example.com" in result
        assert "admin@test.org" in result

    def test_urls(self) -> None:
        text = "Visit https://example.com and http://test.org/path"
        result = extract(text, "urls")
        assert len(result) == 2

    def test_hashtags(self) -> None:
        text = "Check out #Python and #programming"
        result = extract(text, "hashtags")
        assert "#Python" in result

    def test_ips(self) -> None:
        text = "Server at 192.168.1.1 and 10.0.0.1"
        result = extract(text, "ips")
        assert "192.168.1.1" in result


# ── Diff ────────────────────────────────────────────────────────────


class TestDiffTexts:
    def test_identical(self) -> None:
        result = diff_texts("a\nb\nc", "a\nb\nc")
        assert result.similarity == 1.0
        assert result.added == []
        assert result.removed == []

    def test_different(self) -> None:
        result = diff_texts("a\nb", "b\nc")
        assert "a" in result.removed
        assert "c" in result.added
        assert "b" in result.unchanged


# ── Lorem Ipsum ─────────────────────────────────────────────────────


class TestLoremIpsum:
    def test_words(self) -> None:
        result = lorem_ipsum(10, "words")
        assert len(result.split()) == 10

    def test_paragraphs(self) -> None:
        result = lorem_ipsum(3, "paragraphs")
        assert result.count("\n\n") == 2

    def test_zero(self) -> None:
        assert lorem_ipsum(0) == ""


# ── Reverse ─────────────────────────────────────────────────────────


class TestReverseText:
    def test_characters(self) -> None:
        assert reverse_text("hello", "characters") == "olleh"

    def test_words(self) -> None:
        assert reverse_text("hello world", "words") == "world hello"

    def test_lines(self) -> None:
        assert reverse_text("a\nb\nc", "lines") == "c\nb\na"


# ── JSON ────────────────────────────────────────────────────────────


class TestJSON:
    def test_format(self) -> None:
        result = json_format('{"a":1,"b":2}')
        assert '"a": 1' in result
        assert "\n" in result

    def test_minify(self) -> None:
        result = json_minify('{\n  "a": 1,\n  "b": 2\n}')
        assert result == '{"a":1,"b":2}'

    def test_validate_valid(self) -> None:
        assert json_validate('{"key": "value"}') is True

    def test_validate_invalid(self) -> None:
        assert json_validate("{not json}") is False

    def test_format_invalid(self) -> None:
        with pytest.raises(ValueError, match="Invalid JSON"):
            json_format("not json")
