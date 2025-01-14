import os
import subprocess


def get_clipboard_content():
    """Get clipboard content in a cross-platform way"""
    if os.name == "nt":  # Windows
        try:
            # Avoid issues with quotes by using clip.exe instead of PowerShell
            return (
                subprocess.check_output("powershell.exe Get-Clipboard", shell=True)
                .decode("utf-8")
                .strip()
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""
    else:  # Linux
        # Check for xclip first
        if (
            subprocess.run(
                ["which", "xclip"], capture_output=True, check=False
            ).returncode
            == 0
        ):
            try:
                return subprocess.check_output(
                    ["xclip", "-selection", "clipboard", "-o"],
                    stderr=subprocess.DEVNULL,
                ).decode("utf-8")
            except subprocess.CalledProcessError:
                return ""
        # Fall back to xsel
        elif (
            subprocess.run(
                ["which", "xsel"], capture_output=True, check=False
            ).returncode
            == 0
        ):
            try:
                return subprocess.check_output(
                    ["xsel", "-b"], stderr=subprocess.DEVNULL
                ).decode("utf-8")
            except subprocess.CalledProcessError:
                return ""
        return ""  # Return empty string if no clipboard tool is available


def set_clipboard_content(content):
    """Set clipboard content in a cross-platform way"""
    if os.name == "nt":  # Windows
        try:
            # Use echo and clip.exe to handle special characters better
            process = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
            process.communicate(input=content.encode("utf-8"))
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    else:  # Linux
        # Check for xclip first
        if (
            subprocess.run(
                ["which", "xclip"], capture_output=True, check=False
            ).returncode
            == 0
        ):
            try:
                subprocess.run(
                    ["xclip", "-selection", "clipboard"],
                    input=content.encode("utf-8"),
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
                return
            except subprocess.CalledProcessError:
                pass
        # Fall back to xsel
        elif (
            subprocess.run(
                ["which", "xsel"], capture_output=True, check=False
            ).returncode
            == 0
        ):
            try:
                subprocess.run(
                    ["xsel", "-b", "-i"],
                    input=content.encode("utf-8"),
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            except subprocess.CalledProcessError:
                pass
