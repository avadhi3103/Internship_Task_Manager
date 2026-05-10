# Task Management System

A full-stack task management API built with Flask, PostgreSQL, WebSockets, and a vanilla JS frontend.

---

## Features

- JWT-based user authentication (register, login, logout)
- Full task CRUD — add, update, delete, get all tasks
- Each task has title, description, priority, and status
- Analytics module using Pandas and NumPy
- Real-time task updates via WebSockets (Flask-SocketIO)
- Clean responsive frontend in HTML, CSS, and JavaScript
- PostgreSQL database with proper relational schema

---

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python, Flask, Flask-SocketIO     |
| Auth        | Flask-JWT-Extended, Flask-Bcrypt  |
| Database    | PostgreSQL, Flask-SQLAlchemy      |
| Analytics   | Pandas, NumPy                     |
| Frontend    | HTML, CSS, Vanilla JavaScript     |
| Real-time   | WebSockets via Socket.IO          |

---

## Project Structure

```
TASK_MANAGEMENT_SYSTEM/
├── app/
│   ├── __init__.py          # App factory, extension setup, static serving
│   ├── models.py            # User and Task SQLAlchemy models
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py        # /api/auth/register, /login, /me
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── routes.py        # /api/tasks/ CRUD
│   ├── analytics/
│   │   ├── __init__.py
│   │   └── routes.py        # /api/analytics/
│   └── sockets/
│       ├── __init__.py
│       └── events.py        # WebSocket connect/disconnect handlers
├── frontend/
│   ├── index.html           # Single-page UI
│   ├── style.css            # Dark theme styling
│   └── app.js               # Fetch API + Socket.IO client logic
├── .env                     # Secret keys and DB URL (never commit)
├── .gitignore
├── config.py                # Loads config from .env
├── run.py                   # Entry point
├── schema.sql               # Raw PostgreSQL schema
└── requirements.txt
```

---

## Prerequisites

- Python 3.10+
- PostgreSQL 13+ installed and running
- Git

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/avadhi3103/Internship_Task_Manager.git
cd Internship_Task_Manager
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL database

Open pgAdmin or psql and run:

```sql
CREATE DATABASE task_manager;
CREATE USER task_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE task_manager TO task_user;
```

Or run the provided schema file directly:

```bash
psql -U postgres -d task_manager -f schema.sql
```

### 5. Create the `.env` file

Create a file named `.env` in the project root:

```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/task_manager
```

Replace `yourpassword` with your actual PostgreSQL password.

### 6. Run the application

```bash
python run.py
```

Server starts at `http://127.0.0.1:5000`

---

## API Reference

### Auth

| Method | Endpoint               | Description        | Auth Required |
|--------|------------------------|--------------------|---------------|
| POST   | /api/auth/register     | Register new user  | No            |
| POST   | /api/auth/login        | Login, get token   | No            |
| GET    | /api/auth/me           | Get current user   | Yes           |

### Tasks

| Method | Endpoint               | Description        | Auth Required |
|--------|------------------------|--------------------|---------------|
| GET    | /api/tasks/            | Get all tasks      | Yes           |
| POST   | /api/tasks/            | Create task        | Yes           |
| PATCH  | /api/tasks/<id>        | Update task        | Yes           |
| DELETE | /api/tasks/<id>        | Delete task        | Yes           |

### Analytics

| Method | Endpoint               | Description              | Auth Required |
|--------|------------------------|--------------------------|---------------|
| GET    | /api/analytics/        | Get task summary stats   | Yes           |

---

## Request Examples

### Register
```json
POST /api/auth/register
{
  "username": "avadhi",
  "email": "a@a.com",
  "password": "1234"
}
```

### Login
```json
POST /api/auth/login
{
  "email": "a@a.com",
  "password": "1234"
}
```

### Add Task (requires Authorization header)
```json
POST /api/tasks/
Headers: Authorization: Bearer <token>

{
  "title": "My Task",
  "description": "Task details here",
  "priority": "high",
  "status": "pending"
}
```

### Analytics Response
```json
GET /api/analytics/
{
  "total": 5,
  "completed": 2,
  "pending": 2,
  "in_progress": 1,
  "completion_percentage": 40.0,
  "priority_breakdown": {
    "high": 2,
    "medium": 2,
    "low": 1
  }
}
```

---

## WebSocket

Clients connect with their JWT token as auth:

```javascript
const socket = io('http://127.0.0.1:5000', {
  auth: { token: '<access_token>' }
});

socket.on('task_updated', (data) => { /* re-render tasks */ });
socket.on('task_deleted', (data) => { /* remove task from UI */ });
```

Events emitted by server on every task mutation — users only receive events for their own tasks.

---

## Notes

- The `.env` file is excluded from version control via `.gitignore`
- Tokens expire after 15 minutes by default — re-login to get a fresh one
- `db.create_all()` runs on startup and creates tables automatically if they don't exist
- The frontend is served directly by Flask at `http://127.0.0.1:5000`
