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


from typing import List, Dict, Any, Optional
import sqlite3
import json
from datetime import datetime


class Database:
    """Manages SQLite database for user progress and statistics."""
    
    def __init__(self, db_path: str = "data/typing.db") -> None:
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path: str = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        import os
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn: sqlite3.Connection = sqlite3.connect(self.db_path)
        cursor: sqlite3.Cursor = conn.cursor()
        
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
    
    def save_test(
        self,
        user_email: Optional[str],
        wpm: float,
        accuracy: float,
        mistakes: Dict[str, int],
        duration: float
    ) -> None:
        """
        Save typing test results.
        
        Args:
            user_email: User email (None if not logged in)
            wpm: Words per minute
            accuracy: Accuracy percentage
            mistakes: Dictionary of character mistakes
            duration: Test duration in seconds
        """
        conn: sqlite3.Connection = sqlite3.connect(self.db_path)
        cursor: sqlite3.Cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO tests (user_email, timestamp, wpm, accuracy, mistakes, duration)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_email, datetime.now().isoformat(), wpm, accuracy, 
             json.dumps(mistakes), duration)
        )
        
        conn.commit()
        conn.close()
    
    def update_char_stats(
        self,
        user_email: Optional[str],
        char: str,
        is_error: bool
    ) -> None:
        """
        Update character statistics.
        
        Args:
            user_email: User email (None if not logged in)
            char: Character typed
            is_error: Whether this was an error
        """
        conn: sqlite3.Connection = sqlite3.connect(self.db_path)
        cursor: sqlite3.Cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, errors, total_typed FROM character_stats 
               WHERE user_email = ? AND character = ?""",
            (user_email, char)
        )
        row: Optional[tuple] = cursor.fetchone()
        
        if row:
            new_errors: int = row[1] + (1 if is_error else 0)
            new_total: int = row[2] + 1
            cursor.execute(
                """UPDATE character_stats SET errors = ?, total_typed = ?
                   WHERE id = ?""",
                (new_errors, new_total, row[0])
            )
        else:
            cursor.execute(
                """INSERT INTO character_stats (user_email, character, errors, total_typed)
                   VALUES (?, ?, ?, ?)""",
                (user_email, char, 1 if is_error else 0, 1)
            )
        
        conn.commit()
        conn.close()
    
    def get_stats(
        self,
        user_email: Optional[str]
    ) -> Dict[str, Any]:
        """
        Get user statistics.
        
        Args:
            user_email: User email (None if not logged in)
            
        Returns:
            Dictionary containing statistics
        """
        conn: sqlite3.Connection = sqlite3.connect(self.db_path)
        cursor: sqlite3.Cursor = conn.cursor()
        
        if user_email is None:
            cursor.execute(
                """SELECT AVG(wpm), AVG(accuracy), COUNT(*) FROM tests 
                   WHERE user_email IS NULL"""
            )
        else:
            cursor.execute(
                """SELECT AVG(wpm), AVG(accuracy), COUNT(*) FROM tests 
                   WHERE user_email = ?""",
                (user_email,)
            )
        row: Optional[tuple] = cursor.fetchone()
        
        avg_wpm: float = row[0] if row[0] else 0.0
        avg_accuracy: float = row[1] if row[1] else 0.0
        total_tests: int = row[2]
        
        if user_email is None:
            cursor.execute(
                """SELECT character, errors, total_typed FROM character_stats 
                   WHERE user_email IS NULL ORDER BY errors DESC LIMIT 10"""
            )
        else:
            cursor.execute(
                """SELECT character, errors, total_typed FROM character_stats 
                   WHERE user_email = ? ORDER BY errors DESC LIMIT 10""",
                (user_email,)
            )
        problem_chars: List[tuple] = cursor.fetchall()
        
        conn.close()
        
        return {
            "avg_wpm": avg_wpm,
            "avg_accuracy": avg_accuracy,
            "total_tests": total_tests,
            "problem_chars": problem_chars
        }
