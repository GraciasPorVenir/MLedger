import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from ..config import Config


class Connection:
    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self.connect(self.config.db_path)

    def connect(self, db_path: Path) -> None:
        if db_path.suffix == ".sqlite":
            self.close()
            self.conn: sqlite3.Connection = sqlite3.connect(
                db_path, check_same_thread=False
            )
            self.conn.row_factory = sqlite3.Row
            for ddl in (Path(__file__).resolve().parent / "ddl").iterdir():
                if ddl.is_file() and ddl.suffix == ".sql":
                    self.conn.executescript(ddl.read_text())

    @contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor]:
        cursor: sqlite3.Cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def backup(self, db_backup_file: Path | None = None):
        if db_backup_file == None:
            db_backup_file = (
                self.config.db_path.parent
                / f"mledger_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite"
            )
        if db_backup_file.exists():
            db_backup_file.unlink()
        self.conn.execute("VACUUM INTO ?;", (str(db_backup_file),))

    def close(self) -> None:
        if hasattr(self, "conn"):
            self.conn.close()
