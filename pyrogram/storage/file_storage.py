import logging
import os
import sqlite3
from pathlib import Path

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)


UPDATE_STATE_SCHEMA = """
CREATE TABLE update_state
(
    id   INTEGER PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);
"""


class FileStorage(SQLiteStorage):
    FILE_EXTENSION = ".session"

    def __init__(self, name: str, workdir: Path) -> None:
        super().__init__(name)

        self.database = workdir / (self.name + self.FILE_EXTENSION)

    def update(self) -> None:
        version = self.version()

        if version == 1:
            with self.conn:
                self.conn.execute("DELETE FROM peers")

            version += 1

        if version == 2:
            with self.conn:
                self.conn.execute(
                    "ALTER TABLE sessions ADD api_id INTEGER"
                )

            version += 1

        if version == 3:
            with self.conn:
                self.conn.executescript(UPDATE_STATE_SCHEMA)

            version += 1

        self.version(version)

    async def open(self) -> None:
        path = self.database
        file_exists = path.is_file()

        self.conn = sqlite3.connect(
            str(path), timeout=1, check_same_thread=False
        )

        if not file_exists:
            self.create()
        else:
            self.update()

        with self.conn:
            self.conn.execute("VACUUM")

    async def delete(self) -> None:
        os.remove(self.database)
