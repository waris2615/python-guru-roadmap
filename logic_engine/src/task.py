"""Task model with OOP principles."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import sqlite3


@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    status: str  # pending, in_progress, completed
    created_at: str
    updated_at: str

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class TaskDatabase:
    """Context manager for SQLite database."""
    
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self.conn: sqlite3.Connection = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
    
    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        self.conn.commit()
    
    def add_task(self, title: str, description: str = "") -> Task:
        now = datetime.now().isoformat()
        cursor = self.conn.execute(
            "INSERT INTO tasks (title, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (title, description, 'pending', now, now)
        )
        self.conn.commit()
        return Task(cursor.lastrowid, title, description, 'pending', now, now)
    
    def get_all_tasks(self) -> list[Task]:
        cursor = self.conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        return [Task(**dict(row)) for row in cursor.fetchall()]
    
    def update_status(self, task_id: int, status: str) -> bool:
        now = datetime.now().isoformat()
        cursor = self.conn.execute(
            "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
            (status, now, task_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_task(self, task_id: int) -> bool:
        cursor = self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return cursor.rowcount > 0