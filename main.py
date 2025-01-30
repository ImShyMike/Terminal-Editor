"""Terminal editor application file."""

import asyncio
import sys

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Header, Input, TextArea

AUTO_SAVE_INTERVAL = 5  # In minutes


class FileNamePrompt(Screen):
    """File name prompt screen."""

    CSS = """
    Input {
        border: solid #000000;
    }
    """

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self, save=False, read=False):
        super().__init__()
        self.save = save
        self.read = read

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter file name")

    async def action_quit(self):
        """Handle the screen quit action."""
        self.app.pop_screen()

    def on_input_submitted(self, event: Input.Submitted):
        """Handle the input submitted event."""
        self.app.file_name = event.value  # pylint: disable=attribute-defined-outside-init
        self.app.pop_screen()
        if self.save:
            self.app.save_file()
        elif self.read:
            try:
                with open(self.app.file_name, "r", encoding="utf8") as file:
                    content = file.read()
            except FileNotFoundError:
                self.notify(f"File '{self.app.file_name}' not found!")
                return
            self.app.text_area.text = content
            self.app.unsaved_changes = False  # pylint: disable=attribute-defined-outside-init


class TerminalEditor(App):
    """Main application class."""

    CSS = """
    TextArea {
        height: 1fr;
        border: none;
    }
    Footer {
        background: #333333;
        color: white;
        dock: bottom;
    }
    """

    BINDINGS = [
        ("ctrl+s", "save", "Save"),
        ("ctrl+o", "open", "Open"),
        ("ctrl+n", "new", "New"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self, file_name=None):
        super().__init__()
        self.file_name = file_name
        self.unsaved_changes = False
        self.quitting = False

    def compose(self) -> ComposeResult:
        yield Header(icon="", name="Terminal Editor")
        yield Container(
            TextArea(
                soft_wrap=False,
                tab_behavior="indent",
                show_line_numbers=True,
            )
        )
        yield Footer()

    def on_mount(self):
        """Called when the app is mounted."""
        asyncio.create_task(self.auto_save())
        self.text_area = self.query_one(TextArea)  # pylint: disable=attribute-defined-outside-init
        if self.file_name:
            try:
                with open(self.file_name, "r", encoding="utf8") as file:
                    content = file.read()
            except FileNotFoundError:
                self.notify(f"File '{self.file_name}' not found!")
                return
            self.text_area.text = content

    async def auto_save(self):
        """Auto save the file every AUTO_SAVE_INTERVAL minutes."""
        while True:
            await asyncio.sleep(AUTO_SAVE_INTERVAL * 60)
            if self.file_name:
                await self.save_file()

    def on_text_area_changed(self, _: TextArea.Changed) -> None:
        """Called when text is modified in the text area."""
        self.quitting = False  # Reset quitting flag
        self.unsaved_changes = True  # Mark unsaved changes when text is modified

    def action_save(self):
        """Handle the save action."""
        if not self.file_name:
            self.push_screen(FileNamePrompt(save=True))
        else:
            self.save_file()

    def save_file(self):
        """Actually save the file."""
        content = self.text_area.text
        try:
            with open(self.file_name, "w", encoding="utf8") as file:
                file.write(content)
                self.unsaved_changes = False
        except Exception as e:  # pylint: disable=broad-except
            self.notify(f"Failed to save file '{self.file_name}'! ({e})")
        self.notify(f"File '{self.file_name}' saved successfully!")

    def action_open(self):
        """Handle the open action."""
        self.push_screen(FileNamePrompt(read=True))

    def action_new(self):
        """Handle the new action."""
        self.file_name = None
        self.text_area.clear()
        self.push_screen(FileNamePrompt())

    async def action_quit(self):
        """Handle the quit action."""
        if self.quitting:
            self.exit()
            return
        if self.unsaved_changes:
            self.notify("Unsaved changes! Press Ctrl+q again to quit.")
            self.quitting = True
            return
        self.exit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        app = TerminalEditor(sys.argv[1])
    else:
        app = TerminalEditor()
    app.run()
