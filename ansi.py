# CSI Codes (https://en.wikipedia.org/wiki/ANSI_escape_code#Control_Sequence_Introducer_commands)

ESC = "\033["


def flush_print(text):
    """Print text."""
    print(text, end="", flush=True)


def cursor_up(n=1):
    """Move cursor up n lines."""
    return f"{ESC}{n}A"


def cursor_down(n=1):
    """Move cursor down n lines."""
    return f"{ESC}{n}B"


def cursor_forward(n=1):
    """Move cursor forward n columns."""
    return f"{ESC}{n}C"


def cursor_back(n=1):
    """Move cursor back n columns."""
    return f"{ESC}{n}D"


def cursor_next_line(n=1):
    """Move cursor to next line, scrolling if necessary. (Not ANSI.SYS)"""
    return f"{ESC}{n}E"


def cursor_previous_line(n=1):
    """Move cursor to previous line, scrolling if necessary. (Not ANSI.SYS)"""
    return f"{ESC}{n}F"


def cursor_horizontal_absolute(n=1):
    """Move cursor to column n. (Not ANSI.SYS)"""
    return f"{ESC}{n}G"


def cursor_position(n=1, m=1):
    """Move cursor to line n, column m."""
    return f"{ESC}{n};{m}H"


def erase_in_display(n=0):
    """
    Clears part of the screen.

    If n is 0, clear from cursor to end of screen.
    If n is 1, clear from cursor to beginning of the screen.
    If n is 2, clear entire screen (and moves cursor to upper left on DOS ANSI.SYS).
    If n is 3, clear entire screen and delete all lines saved in the scrollback buffer (this feature was added for xterm and is supported by other terminal applications).
    """
    return f"{ESC}{n}J"


def erase_in_line(n=0):
    """
    Erases part of the line.

    If n is 0 (or missing), clear from cursor to the end of the line.
    If n is 1, clear from cursor to beginning of the line.
    If n is 2, clear entire line. Cursor position does not change.
    """
    return f"{ESC}{n}K"


def scroll_up(n=1):
    """Scroll up n lines. (Not ANSI.SYS)"""
    return f"{ESC}{n}S"


def scroll_down(n=1):
    """Scroll down n lines. (Not ANSI.SYS)"""
    return f"{ESC}{n}T"


def horizontal_vertical_position(n=1, m=1):
    """Move cursor to line n, column m."""
    return f"{ESC}{n};{m}f"


def select_graphic_rendition(n=0):
    """Select graphic rendition."""
    return f"{ESC}{n}m"


def aux_port_on():
    """Auxiliary port on."""
    return f"{ESC}5i"


def aux_port_off():
    """Auxiliary port off."""
    return f"{ESC}4i"


def device_status_report():
    """Device status report."""
    return f"{ESC}6n"


def save_cursor_position():
    """Save cursor position."""
    return f"{ESC}s"


def restore_cursor_position():
    """Restore cursor position."""
    return f"{ESC}u"


# C0 codes (https://en.wikipedia.org/wiki/ANSI_escape_code#C0_control_codes)


def bell():
    """Bell"""
    return "\007"


def backspace():
    """Backspace"""
    return "\008"


def tab():
    """Tab"""
    return "\009"


def linefeed():
    """Linefeed"""
    return "\010"


def form_feed():
    """Form feed"""
    return "\012"


def carriage_return():
    """Carriage return"""
    return "\013"


def escape():
    """Escape"""
    return "\033"


def delete():
    """Delete"""
    return "\07f"
