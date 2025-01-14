import re

import ansi

# Full keyword list
KEYWORDS = [
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
]


# Class to mimic a match object
class StringMatch:
    def __init__(self, start, end):
        self.start_pos = start
        self.end_pos = end

    def start(self):
        return self.start_pos

    def end(self):
        return self.end_pos


def apply_colors(text, matches, color, reset_color):
    """Apply colors to text matches"""

    output = list(text)

    offset = 0
    for match in matches:
        output.insert(match.start() + offset, ansi.select_graphic_rendition(color))
        offset += 1
        output.insert(match.end() + offset, ansi.select_graphic_rendition(reset_color))
        offset += 1

    return "".join(output)


def parse_keywords(text):
    """Parse text matches and highlight keywords"""

    # Create a regex pattern that matches whole words only
    pattern = r"\b(" + "|".join(map(re.escape, KEYWORDS)) + r")\b"

    # Find all matches with their positions
    matches = list(re.finditer(pattern, text))

    return apply_colors(text, matches, 36, 39)  # Cyan


def parse_strings(text):
    """Parse text matches and highlight strings"""

    # Pattern matches single/triple quotes with proper escaping
    pattern = r"""
        # Triple-quoted strings (both single and double)
        \"""(?:(?!\""").)*(?:\"""|\Z) |
        \'\'\'(?:(?!\'\'\').)*(?:\'\'\'|\Z) |
        
        # Single-quoted strings
        \"(?:\\.|[^\"\\])*(?:\"|\Z) |
        \'(?:\\.|[^\'\\])*(?:\'|\Z)
    """

    # First find all complete strings
    matches = []
    for match in re.finditer(pattern, text, re.VERBOSE | re.DOTALL):
        # Verify this match isn't inside another string type
        valid = True
        start = match.start()

        # Check if this position is inside any previous match
        for prev_match in matches:
            if prev_match.start() < start < prev_match.end():
                valid = False
                break

        if valid:
            matches.append(match)

    return apply_colors(text, matches, 35, 39)  # Magenta


def parse_text(text):
    """Parse text and apply all highlighting"""
    # First apply syntax highlighting
    highlighted_text = parse_keywords(text)
    highlighted_text = parse_strings(highlighted_text)

    return highlighted_text
