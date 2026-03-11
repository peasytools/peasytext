# peasytext — Pure Python Text Toolkit Demo
Output demo.gif

Set FontSize 20
Set Width 1000
Set Height 580
Set Shell "zsh"
Set Theme "Catppuccin Mocha"
Set TypingSpeed 30ms
Set Padding 24

Type "uv run --with peasytext python3"
Enter
Sleep 2.5s

Type "from peasytext import to_case, slugify, count_text, lorem_ipsum"
Enter
Sleep 1s

Type "# Convert text to camelCase"
Enter
Sleep 0.5s

Type "to_case('hello world from peasy', 'camel')"
Enter
Sleep 1.5s

Type "# Generate URL-safe slug"
Enter
Sleep 0.5s

Type "slugify('Hello World — Special Characters! @#$')"
Enter
Sleep 1.5s

Type "# Word & character count"
Enter
Sleep 0.5s

Type "count_text('The quick brown fox jumps over the lazy dog')"
Enter
Sleep 2s

Type "# Generate Lorem Ipsum"
Enter
Sleep 0.5s

Type "lorem_ipsum(words=12)"
Enter
Sleep 2s

Type "exit()"
Enter
Sleep 1s
