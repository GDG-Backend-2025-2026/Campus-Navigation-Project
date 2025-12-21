# Campus Navigation API

Flask + PostgreSQL API for managing colleges in a campus navigation system.

## Quick Start

1. Create PostgreSQL database: `createdb campus_nav`
2. Copy `.env.example` to `.env` and update values
3. `pip install -r requirements.txt`
4. `python run.py`

## API Endpoints

**Auth:**
- `POST /api/login`

**Colleges:**
- `GET /api/colleges`
- `GET /api/colleges/<id>`
- `POST /api/colleges` (JWT required)
- `PUT /api/colleges/<id>` (JWT required)
- `DELETE /api/colleges/<id>` (JWT required)

Demo login: `osazuwa` / `osazuwa1234`
