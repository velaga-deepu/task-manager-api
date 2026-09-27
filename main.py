"""
Advanced To-Do List API
A FastAPI + SQLite backend for a to-do list with priorities and due dates.
Replaces plain localStorage with a real persisted database and REST API.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI(title="Advanced To-Do List API")

# Allow the frontend (served separately, e.g. via Live Server) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "todo.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            priority TEXT NOT NULL DEFAULT 'medium',
            due_date TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


class TaskCreate(BaseModel):
    text: str
    priority: str = "medium"   # low | medium | high
    due_date: Optional[str] = None   # e.g. "2026-10-01"


class TaskUpdate(BaseModel):
    text: Optional[str] = None
    done: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None


@app.get("/tasks")
def list_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (text, priority, due_date) VALUES (?, ?, ?)",
        (task.text, task.priority, task.due_date),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, **task.dict(), "done": False}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    conn = get_connection()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    updated = {
        "text": task.text if task.text is not None else existing["text"],
        "done": int(task.done) if task.done is not None else existing["done"],
        "priority": task.priority if task.priority is not None else existing["priority"],
        "due_date": task.due_date if task.due_date is not None else existing["due_date"],
    }

    conn.execute(
        "UPDATE tasks SET text=?, done=?, priority=?, due_date=? WHERE id=?",
        (updated["text"], updated["done"], updated["priority"], updated["due_date"], task_id),
    )
    conn.commit()
    conn.close()
    return {"id": task_id, **updated}


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = get_connection()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return None


@app.delete("/tasks")
def clear_completed():
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE done = 1")
    conn.commit()
    conn.close()
    return {"message": "Completed tasks cleared"}
