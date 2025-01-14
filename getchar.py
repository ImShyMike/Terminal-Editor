try:
    import termios
    import tty
except ImportError:
    pass
try:
    import msvcrt
except ImportError:
    pass
import sys


# https://www.jonwitts.co.uk/archives/896
def getch_unix():
    """Get character from Unix console"""

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

        # Handle escape sequences for special keys
        if ch == "\x1b":
            # Read potential second and third chars of escape sequence
            ch2 = sys.stdin.read(1)
            if ch2 == "[":
                ch3 = sys.stdin.read(1)
                # Map arrow keys and other special keys
                special_keys = {
                    "A": "UP",
                    "B": "DOWN",
                    "D": "LEFT",
                    "C": "RIGHT",
                    "H": "HOME",
                    "F": "END",
                    "5": "PGUP",
                    "6": "PGDN",
                    "3": "DEL",
                    "1": "SHIFT_DOWN",
                    "2": "SHIFT_UP",
                }
                return special_keys.get(ch3, f"SPECIAL_{ord(ch3)}")
            return "ESC"

        # Handle enter key (CR)
        elif ch == "\r":
            return "ENTER"
        # Handle tab key
        elif ch == "\t":
            return "TAB"
        # Handle backspace
        elif ch == "\x7f":  # Unix backspace is 0x7f
            return "BACKSPACE"
        # Handle Ctrl+key combinations
        elif ord(ch) < 32:
            return f"CTRL_{chr(ord(ch) + 64)}"

        # Regular character
        return ch

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def getch_win():
    """Get character from Windows console"""

    # Get first character
    ch = msvcrt.getch()

    # Handle special keys (like arrows) that start with b'\xe0' or b'\x00'
    if ch in (b"\xe0", b"\x00"):
        # Get the second character that specifies which special key
        special = msvcrt.getch()

        # Map special keys to readable names
        special_keys = {
            b"H": "UP",
            b"P": "DOWN",
            b"K": "LEFT",
            b"M": "RIGHT",
            b"G": "HOME",
            b"O": "END",
            b"I": "PGUP",
            b"Q": "PGDN",
            b"S": "DEL",
            b"R": "INSERT",
            b"-": "SHIFT_DOWN",
            b"+": "SHIFT_UP",
        }
        return special_keys.get(special, f"SPECIAL_{str(special)}")

    # Handle Ctrl+key combinations and special keys
    elif ch < b" ":
        # Handle enter key (CR)
        if ch == b"\r":
            return "ENTER"

        # Handle tab key
        if ch == b"\t":
            return "TAB"

        # Handle escape key
        if ch == b"\x1b":
            return "ESC"

        # Handle backspace
        if ch == b"\x08":
            return "BACKSPACE"

        # Handle other control characters
        return f"CTRL_{chr(ord(ch) + 64)}"

    # Regular character
    return ch.decode()
