# Task Manager API

A full-stack task management app with a real backend — not just browser
storage. Add tasks with priority levels and due dates, mark them done, and
everything persists in a SQLite database via a REST API.

## Features
- Add, complete, and delete tasks
- Priority levels (low / medium / high) with color-coded badges
- Due dates per task
- Dark mode toggle
- Data persisted server-side in SQLite

## Built With
- **Backend:** FastAPI, SQLite, Pydantic
- **Frontend:** HTML, CSS, JavaScript (fetch API)

## How It Works
The frontend calls a FastAPI REST API (`GET`/`POST`/`PUT`/`DELETE /tasks`),
which reads and writes to a SQLite database, so tasks persist server-side
rather than relying on browser storage.

## Installation & Running

**Backend:**
```
pip install -r requirements.txt
uvicorn main:app --reload
```
Runs at `http://127.0.0.1:8000`

**Frontend:**
Open `index.html` in your browser (with the backend running).

## Project Structure
```
task-manager-api/
│
├── main.py
├── requirements.txt
└── index.html
```

## Purpose
Built to practice designing a full REST API with FastAPI and SQLite,
covering CRUD operations, request validation with Pydantic, and connecting
a frontend to a live backend.
