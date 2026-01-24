import logging
import textwrap
import tempfile
import json

from datetime import datetime
from pathlib import Path

from enq.cli.editor import Editor

logger = logging.getLogger(__name__)

def extract_title_from_content(content: str) -> tuple[str, str]:
    title = ""
    remaining_lines = []
    found_content = False

    if not content.strip():
        return title, ""

    for line in content.splitlines():
        is_whitespace = not line.strip()

        if not found_content:
            if is_whitespace:
                continue

        found_content = True
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue

        remaining_lines.append(line)

    return title, "\n".join(remaining_lines).strip()

class EntryHandler:
    def __init__(self, config, storage):
        self.config = config
        self.storage = storage

    def create_entry_from_editor(self):

        editor = Editor(self.config.settings["editor"])

        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=self.config.settings["extension"], delete=False
        ) as tf:
            temp_path = Path(tf.name)

            tf.write("# Put title here, or remove me...\n\n")

        try:
            editor.open(temp_path)

            content = temp_path.read_text(encoding="utf-8")

            title, message = extract_title_from_content(content)
            timestamp = str(datetime.now().replace(microsecond=0))

            logger.debug(f"User wrote: {json.dumps({"title": title, "message": message, "timestamp": timestamp})}")

            if message != "":
                self.storage.add_entry(title, message, timestamp)

        finally:
            if temp_path.exists():
                temp_path.unlink()

class Entry:

    def __init__(self, title, message, timestamp):
        pass

