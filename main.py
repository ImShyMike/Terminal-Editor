import os
import sys
import atexit

import ansi
import getchar
import syntax_higlight.python
import clipboard
import cursor

if os.name == "nt":  # Windows
    getch = getchar.getch_win
    os.system("")  # Fix for escape codes
else:  # Unix-like
    getch = getchar.getch_unix

TAB_TEXT = "    "
UPDATE_RATE = 1 / 30

cursor_obj = cursor.Cursor()

cursor_position = (1, 1)


def main():
    """Main editor logic"""

    text_buffer = ""
    display = ""
    ansi.flush_print(ansi.erase_in_display(2) + ansi.cursor_position(1, 1))

    while True:
        try:
            char = getch()

            # Regular character input
            if len(char) == 1:
                text_buffer = cursor_obj.insert_text(text_buffer, char)
            elif char == "TAB":
                text_buffer = cursor_obj.insert_text(text_buffer, TAB_TEXT)
            elif char == "ENTER":
                text_buffer = cursor_obj.insert_text(text_buffer, "\n")
            elif char == "ESC":
                exit_program()
            elif char == "CTRL_C":
                clipboard.set_clipboard_content(text_buffer)
            elif char == "CTRL_V":
                text_buffer = cursor_obj.insert_text(
                    text_buffer, clipboard.get_clipboard_content()
                )
            elif char == "BACKSPACE":
                text_buffer = cursor_obj.backspace(text_buffer)
            elif char == "LEFT":
                cursor_obj.move_left(text_buffer)
            elif char == "RIGHT":
                cursor_obj.move_right(text_buffer)
            elif char == "UP":
                cursor_obj.move_up(text_buffer)
            elif char == "DOWN":
                cursor_obj.move_down(text_buffer)

            # Modified rendering
            display = ansi.erase_in_display(0) + ansi.cursor_position(1, 1)
            display += syntax_higlight.python.parse_text(text_buffer)

            cols, lines = os.get_terminal_size()
            line, col = cursor_obj.get_position()

            display += ansi.cursor_position(1, 1) + "\n" * (
                lines - 1
            ) + f"({col}, {line}) / ({cols}, {lines})".rjust(cols)

            ansi.flush_print(display + ansi.cursor_position(line, col))

        except KeyboardInterrupt:
            pass


def exit_program():
    """Exit editor"""
    ansi.flush_print(ansi.erase_in_display(2) + ansi.cursor_position(1, 1))
    sys.exit(0)


def save_current_file():
    """TODO"""


if __name__ == "__main__":
    atexit.register(save_current_file)
    main()
