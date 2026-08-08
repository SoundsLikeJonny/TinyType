#      TinyType is a minimal typing test software that sits in the corner of your screen while you work!
#      Copyright (C) 2026  Jon Evans
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.


from typing import List, Dict, Any, Optional, Tuple
import sqlite3
import json
import os
import queue
import threading
from datetime import datetime


def _user_data_dir() -> str:
    """Return the per-user data directory: %APPDATA%\\TinyType on Windows."""
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(base, "TinyType")


class Database:
    """Manages SQLite database for user progress and statistics.

    All writes are dispatched to a background thread via a queue so that
    the UI thread (and therefore typing) is never blocked by disk I/O.
    """

    _STOP = object()  # sentinel that shuts the writer thread down

    def __init__(self, db_path: str = "") -> None:
        if not db_path:
            db_path = os.path.join(_user_data_dir(), "typing.db")
        self.db_path: str = db_path
        self._migrate_legacy()
        self._init_db()

        self._write_queue: queue.Queue = queue.Queue()
        self._writer_thread = threading.Thread(
            target=self._writer_loop, daemon=True, name="db-writer"
        )
        self._writer_thread.start()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _migrate_legacy(self) -> None:
        """Copy database from old data/ directory if the new location is empty."""
        if os.path.exists(self.db_path):
            return
        legacy = os.path.join("data", "typing.db")
        if os.path.exists(legacy):
            import shutil
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            shutil.copy2(legacy, self.db_path)

    def _init_db(self) -> None:
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = self._open_conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT,
                timestamp TEXT,
                wpm REAL,
                accuracy REAL,
                mistakes TEXT,
                duration REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS character_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT,
                character TEXT,
                errors INTEGER,
                total_typed INTEGER
            )
        """)
        conn.commit()
        conn.close()

    # ------------------------------------------------------------------
    # Background writer
    # ------------------------------------------------------------------

    def _open_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    def _writer_loop(self) -> None:
        """Runs on the background thread; drains the write queue serially."""
        conn = self._open_conn()
        while True:
            item = self._write_queue.get()
            if item is self._STOP:
                conn.close()
                break
            op, args = item
            try:
                if op == "save_test":
                    self._do_save_test(conn, *args)
                elif op == "update_char_stats":
                    self._do_update_char_stats(conn, *args)
            except Exception:
                pass  # never crash the writer thread
            finally:
                self._write_queue.task_done()

    def _do_save_test(
        self,
        conn: sqlite3.Connection,
        user_email: Optional[str],
        wpm: float,
        accuracy: float,
        mistakes: Dict[str, int],
        duration: float,
    ) -> None:
        conn.execute(
            """INSERT INTO tests (user_email, timestamp, wpm, accuracy, mistakes, duration)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_email, datetime.now().isoformat(), wpm, accuracy,
             json.dumps(mistakes), duration),
        )
        conn.commit()

    def _do_update_char_stats(
        self,
        conn: sqlite3.Connection,
        user_email: Optional[str],
        char: str,
        is_error: bool,
    ) -> None:
        row = conn.execute(
            """SELECT id, errors, total_typed FROM character_stats
               WHERE user_email IS ? AND character = ?""",
            (user_email, char),
        ).fetchone()
        if row:
            conn.execute(
                """UPDATE character_stats SET errors = ?, total_typed = ? WHERE id = ?""",
                (row[1] + (1 if is_error else 0), row[2] + 1, row[0]),
            )
        else:
            conn.execute(
                """INSERT INTO character_stats (user_email, character, errors, total_typed)
                   VALUES (?, ?, ?, ?)""",
                (user_email, char, 1 if is_error else 0, 1),
            )
        conn.commit()

    # ------------------------------------------------------------------
    # Public write API  (UI thread — non-blocking)
    # ------------------------------------------------------------------

    def save_test(
        self,
        user_email: Optional[str],
        wpm: float,
        accuracy: float,
        mistakes: Dict[str, int],
        duration: float,
    ) -> None:
        self._write_queue.put(("save_test", (user_email, wpm, accuracy, mistakes, duration)))

    def update_char_stats(
        self,
        user_email: Optional[str],
        char: str,
        is_error: bool,
    ) -> None:
        self._write_queue.put(("update_char_stats", (user_email, char, is_error)))

    # ------------------------------------------------------------------
    # Public read API  (UI thread — uses a short-lived read connection)
    # ------------------------------------------------------------------

    def get_stats(self, user_email: Optional[str]) -> Dict[str, Any]:
        conn = self._open_conn()
        try:
            if user_email is None:
                row = conn.execute(
                    "SELECT AVG(wpm), AVG(accuracy), COUNT(*) FROM tests WHERE user_email IS NULL"
                ).fetchone()
                chars = conn.execute(
                    """SELECT character, errors, total_typed FROM character_stats
                       WHERE user_email IS NULL ORDER BY errors DESC LIMIT 10"""
                ).fetchall()
            else:
                row = conn.execute(
                    "SELECT AVG(wpm), AVG(accuracy), COUNT(*) FROM tests WHERE user_email = ?",
                    (user_email,),
                ).fetchone()
                chars = conn.execute(
                    """SELECT character, errors, total_typed FROM character_stats
                       WHERE user_email = ? ORDER BY errors DESC LIMIT 10""",
                    (user_email,),
                ).fetchall()
        finally:
            conn.close()

        return {
            "avg_wpm": row[0] or 0.0,
            "avg_accuracy": row[1] or 0.0,
            "total_tests": row[2],
            "problem_chars": chars,
        }

    # ------------------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Flush pending writes and stop the background thread cleanly."""
        self._write_queue.put(self._STOP)
        self._writer_thread.join(timeout=5)
