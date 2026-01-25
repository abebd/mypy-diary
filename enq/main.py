import logging

from importlib.metadata import version as get_version

from enq.core.entry import EntryHandler
from enq.cli.args import parse_args
from enq.core.logger import setup_logging
from enq.core.config import Config
from enq.cli.menu import MenuHandler
from enq.cli.interface import ui
from enq.storage.database import DatabaseStorage
from enq.storage.file import FileStorage

logger = logging.getLogger(__name__)


class App:
    def __init__(self):
        self.args = parse_args()

        setup_logging(self.args.verbose)

        logger.debug(f"-----| Starting run @ enq-{get_version('enq')} |-----")
        logger.debug(f"Current state: {ui.state}")
        logger.debug(f"Args passed from user: {self.args}")

        self.config = Config(self.args.config_file)

        if self.config.settings["storage_mode"] == "database":
            logger.debug("Using storage type database")
            self.storage = DatabaseStorage(self.config)
        else:
            logger.debug("Using storage type file")
            self.storage = FileStorage(self.config)

        self.entry_handler = EntryHandler(self.config, self.storage)
        self.menu_handler = MenuHandler(self, self.config)

    def run(self):
        ran_something = False

        if self.args.read_entries:
            ran_something = True
            self.entry_handler.select_and_open_entry()

        if self.args.message:
            ran_something = True
            self.entry_handler.create_entry_from_string(self.args.message)

        if self.args.new:
            ran_something = True
            self.entry_handler.create_entry_from_editor()

        # If nothing ran, open the interactive menu
        if not ran_something:
            self.menu_handler.run()


def main():
    app = App()
    app.run()
