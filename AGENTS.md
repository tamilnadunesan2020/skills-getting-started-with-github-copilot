# AI Agent Instructions for Mergington High School Activities API

## Project Overview

This is a **FastAPI web application** for managing high school extracurricular activities. Students can view available activities and sign up for them through a simple web interface.

- **Stack**: FastAPI (backend) + HTML/CSS/JavaScript (frontend)
- **Data**: In-memory only (resets on server restart)
- **Type**: Educational/learning project

## Quick Start

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the application:**
```bash
cd src && python app.py
```

Server runs on `http://localhost:8000`. The API documentation is available at `/docs` (Swagger UI).

## Project Structure

```
src/
├── app.py              # FastAPI application with all endpoints and data
├── static/
│   ├── index.html      # Main HTML page
│   ├── app.js          # Frontend logic (fetches activities, handles signup)
│   └── styles.css      # CSS styling
└── README.md           # API documentation
```

## Key Concepts

### Data Model

**Activities** - identified by name:
- `description`: What the activity is about
- `schedule`: When it meets
- `max_participants`: Capacity limit
- `participants`: List of student emails currently signed up

**Participants** - identified by email (no separate student storage)

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET /activities` | Fetch all activities | Returns activity dict with details and participant lists |
| `POST /activities/{activity_name}/signup?email=...` | Sign up for activity | Adds email to participants list |

## Development Conventions

- **Error Handling**: Basic validation only (activity existence check)
- **Data Persistence**: None - all data is in-memory Python dict
- **Validation**: Email format validation is client-side only
- **Frontend Communication**: Fetch API for async requests to backend

## Common Tasks

**Add a new activity:**
- Modify `activities` dict in `app.py`

**Update activity details:**
- Edit the activity dict entry in `app.py`

**Modify frontend behavior:**
- `app.js` contains all JavaScript logic
- `index.html` contains the page structure
- `styles.css` contains styling

**Test changes:**
- Run `pytest` (pytest.ini configured with src/ in pythonpath)
- Use `/docs` endpoint to test API manually during development

## Important Notes

- ⚠️ This is a learning project - error handling is minimal
- 📝 No database - changes are lost on server restart
- 🔒 No authentication or validation beyond existence checks
- 📱 Frontend is basic - suitable for simple enhancements

## Common Pitfalls

- **Data Loss**: In-memory data means signup lists reset when server restarts
- **Duplicate Signups**: No check to prevent the same email signing up twice for an activity
- **Capacity Enforcement**: Signup endpoint doesn't validate if activity is full
