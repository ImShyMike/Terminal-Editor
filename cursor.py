class Cursor:
    def __init__(self):
        self.line = 0  # Current line number (0-based)
        self.column = 0  # Current column number (0-based)
        self.selection_start = None  # (line, column) tuple for selection start

    def move_left(self, text_buffer):
        if self.column > 0:
            self.column -= 1
        elif self.line > 0:
            # Move to end of previous line
            self.line -= 1
            lines = text_buffer.split("\n")
            self.column = len(lines[self.line])

    def move_right(self, text_buffer):
        lines = text_buffer.split("\n")
        if self.line >= len(lines):
            return

        current_line = lines[self.line]
        if self.column < len(current_line):
            self.column += 1
        elif self.line < len(lines) - 1:
            # Move to start of next line
            self.line += 1
            self.column = 0

    def move_up(self, text_buffer):
        lines = text_buffer.split("\n")
        if self.line > 0:
            self.line -= 1
            # Adjust column if new line is shorter
            self.column = min(self.column, len(lines[self.line]))

    def move_down(self, text_buffer):
        lines = text_buffer.split("\n")
        if self.line < len(lines) - 1:
            self.line += 1
            # Adjust column if new line is shorter
            self.column = min(self.column, len(lines[self.line]))

    def insert_text(self, text_buffer, text):
        lines = text_buffer.split("\n")
        if self.line >= len(lines):
            return text_buffer + text

        current_line = lines[self.line]
        before = current_line[: self.column]
        after = current_line[self.column :]

        if "\n" in text:
            # Handle multiline insertion
            inserted_lines = text.split("\n")
            lines[self.line] = before + inserted_lines[0]
            lines[self.line + 1 : self.line + 1] = inserted_lines[1:]
            last_line = lines[self.line + len(inserted_lines) - 1]
            lines[self.line + len(inserted_lines) - 1] = last_line + after

            self.line += len(inserted_lines) - 1
            self.column = len(inserted_lines[-1])
        else:
            # Single line insertion
            lines[self.line] = before + text + after
            self.column += len(text)

        return "\n".join(lines)

    def backspace(self, text_buffer):
        if self.column == 0 and self.line == 0:
            return text_buffer

        lines = text_buffer.split("\n")
        if self.column > 0:
            # Delete character in current line
            current_line = lines[self.line]
            lines[self.line] = (
                current_line[: self.column - 1] + current_line[self.column :]
            )
            self.column -= 1
        else:
            # Join with previous line
            previous_line = lines[self.line - 1]
            self.column = len(previous_line)
            lines[self.line - 1] = previous_line + lines[self.line]
            lines.pop(self.line)
            self.line -= 1

        return "\n".join(lines)

    def get_position(self):
        # Convert to 1-based coordinates for ANSI
        return (self.line + 1, self.column + 1)
