# School Direction Backend

Flask REST API for the Campus Navigation Project built by the GDG Backend Track.
This service powers the card based navigation system used to locate buildings and lecturer offices on campus.

## Features

• JWT based admin authentication
• CRUD for buildings, colleges, departments and lecturers
• Route and route card management
• PostgreSQL database integration
• Clean project structure with blueprints
• Organized Git workflow with protected branches and PR reviews

---

## Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/GDG-Backend-2025-2026/Campus-Navigation-Project.git
cd <repo-name>
```

## 2. Create and activate a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Mac or Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Set environment variables

Create a `.env` file in the root.

Example

```ini
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@host:port/dbname
JWT_SECRET=your-jwt-secret
```

## 5. Initialize the database

If using Flask Migrate:

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

If using raw SQL, run your schema file manually.

## 6. Start the development server

```bash
python app.py
```

Server will be available on
`http://127.0.0.1:5000`

---

## Project Structure

Example structure your team should follow:

```text
project/
    app.py              # Entry point
    config.py           # Config + env handling
    models/             # SQLAlchemy models
        __init__.py
        building.py
        college.py
        department.py
        lecturer.py
        route.py
        route_card.py
    routes/             # All endpoint routes
        __init__.py
        buildings.py
        colleges.py
        departments.py
        lecturers.py
        routes.py
        auth.py
    utils/
        __init__.py
        db.py           # SQLAlchemy init
        auth.py         # JWT helper functions
    migrations/         # When using Flask-Migrate
    requirements.txt
    README.md
    .env
```

---

## Git Workflow for Contributors

To keep the repository clean, everyone must follow these rules.

## Branching Rules

1. Never push code directly to main or develop.
2. Always create your branch from develop.
3. Use this name format:

```text
feature/<your-name>/<short-description>
```

Examples
feature/treasure/buildings-crud
feature/gbeniga/auth
feature/cyrus/lecturer-crud

## Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-name/your-task
```

## Commit Message Rules

Each commit must start with your name in brackets.

Examples

```text
[Treasure] added building CRUD
[Ore] created initial models
[Gbemiga] implemented JWT login
```

Commits should be clear and short.

## Pushing Your Branch

```bash
git push -u origin feature/your-name/your-task
```

---

## Pull Request Rules

1. Your PR must target the develop branch.
2. Fill the PR template with a summary and test steps.
3. PR must be reviewed and approved before merge.
4. Only Leads (Bayode and Julia) can merge.
5. Resolve all comments before requesting another review.

---

## Environment Secrets

Do not commit your `.env` file.
All secrets must be stored inside GitHub Actions secrets or Render environment variables.

---

## Running Tests (if tests exist)

```bash
pytest
```

---

## Contributors

GDG Backend Track 2025/2026
Backend Leads: Bayode and Julia
