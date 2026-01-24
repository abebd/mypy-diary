import sqlite3
import os
import logging

from pathlib import Path
from enq.storage.base import Storage

logger = logging.getLogger(__name__)

class DatabaseStorage(Storage):
    def __init__(self, config):
        self.config = config
        self.db_path = Path(self.config.paths["diary_db"]).expanduser()
        self.schemas_path = Path(__file__).parent / "schemas"
        self.connection = None
        self._setup_database()

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def run_script(self, script):
        
        if not os.path.exists(script):
            raise FileNotFoundError(f"Unable to find file {script}")

        with open(script, "r") as f:
            sql = f.read()

        try:
            self.connection.executescript(sql)
            self.connection.commit()
            logger.debug(f"Executed script {script}")
        except sqlite3.Error as e:
            logger.error(f"Unable to execute script {script}, {e}")

    def _setup_database(self):

        if not os.path.exists(self.db_path):
            logger.debug(f"Unable to find database {self.db_path}, creating it.")

        self.connection = sqlite3.connect(self.db_path)

        for script in os.listdir(self.schemas_path):
            self.run_script(Path(self.schemas_path / script))

    def add_entry(self, title, body, timestamp):
        entry_date, entry_time = timestamp.split(" ")

        query = """
        INSERT INTO entries (entry_date, entry_time, title, body)
        VALUES (?, ?, ?, ?)
        """

        if title == "Put title here, or remove me...":
            title = ""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (entry_date, entry_time, title, body))
            self.connection.commit()

            new_id = cursor.lastrowid

            logger.debug(f"Inserted entry for timestamp {entry_date} {entry_time} at id {str(new_id)}")

        except sqlite3.Error as e:
            logger.error(f"Failed to insert entry into database: {e}")


    def open_entry(self, title, message, timestamp):
        pass

    def get_entries(self) -> list:
        query = """
        INSERT INTO entries (entry_date, entry_time, title, body)
        VALUES (?, ?, ?, ?)
        """
        pass

