# REST API Learning Project

This repository is a graduating-student learning project for building REST APIs with Python and Flask.

The work is split into three phases. Each phase adds new skills. Phase 3 is still in progress.

---

## What is this project?

The focus is on how backends work: HTTP methods, JSON, databases, and security. The repo shows progress step by step.

| Phase | Status | Main idea |
|-------|--------|-----------|
| [Phase 1](#phase-1---first-rest-api-in-memory) | Done | Simple API with data in memory |
| [Phase 2](#phase-2---database-and-authentication) | Done | API with MySQL database and login (JWT) |
| [Phase 3](#phase-3---job-application-tracker-in-progress) | In progress | Full product: job application tracker |

---

## Project structure

```
.
|-- README.md
|-- phase1.py                   # Phase 1 - one file, in-memory data
`-- phase2/                     # Phase 2 - Flask app + MySQL + Docker
    |-- Dockerfile
    |-- app/                    # API code (routes, models, seed)
    |-- docker-compose.yml
    |-- requirements.txt
    `-- wait-for-db.py
```

Phase 3 will get its own folder when development starts (for example `phase3/`).

---

## Phase 1 - First REST API (in memory)

**Goal:** Understand basic REST ideas without a database.

**Features:**
- Flask app in one file: `phase1.py`
- `GET /` - hello message
- `GET /users` - list all users
- `GET /users?name=...` - find user by name
- `GET /users?limit=...&page=...` - pagination
- `POST /users` - add new user
- `GET /users/<id>`, `PUT /users/<id>`, `DELETE /users/<id>` - one user

**Data:** Users live in a Python list inside the app. When the server stops, data is gone.

**How to run:**

```bash
pip install flask
python phase1.py
```

The server runs on `http://127.0.0.1:5000` (Flask default).

Use **Postman** to send requests and check responses (see section [*Test the API with Postman*](#test-the-api-with-postman) below).

**Topics covered:**
- HTTP methods: GET, POST, PUT, DELETE
- JSON request and response
- Status codes (200, 201, 400, 404)

---

## Phase 2 - Database and authentication

**Goal:** Build an API that saves data in MySQL and protects some routes with JWT.

**Features:**
- Flask app split into modules: `app.py`, `models.py`, `routes.py`, `seed.py`
- SQLAlchemy ORM - `User` model (id, name, email, password)
- MySQL 8 in Docker
- Docker Compose - API + database together
- JWT login - token for protected profile route

**Main endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET, POST | `/users` | List users / create user |
| GET, PUT, DELETE | `/users/<id>` | One user |
| POST | `/users/login` | Login, get JWT token |
| GET | `/users/profile` | Profile (needs `Authorization: Bearer <token>`) |

**Tech stack:**
- Python 3.10, Flask, Flask-SQLAlchemy
- MySQL, PyMySQL
- PyJWT
- Docker, Docker Compose

**How to run (with Docker):**

1. Go to the `phase2` folder.
2. Create a `.env` file. Required variables include `DB_URL`, `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`.
3. Start services:

```bash
cd phase2
docker compose up --build
```

API is on `http://localhost:5000`.

Use **Postman** to test endpoints and JWT login (see section [*Test the API with Postman*](#test-the-api-with-postman) below).

**Note:** On start, the app runs `db.drop_all()` and `db.create_all()` and seeds sample users. This is good for learning, but not for production.

**Topics covered:**
- Connect API to a real database
- Use environment variables
- Basic auth with JWT
- Run app in containers

---

## Phase 3 - Job application tracker (in progress)

**Status:** Work in progress. Code is not finished yet.

**Goal:** Build a small product, not only exercises. The result will be like an **application tracker** for job search.

**Planned features (ideas):**
- Save job applications (company, role, date, status)
- Update status: applied, interview, offer, rejected
- Notes and deadlines
- Reuse Phase 1 and Phase 2 skills (REST API, database, auth)

Phase 3 code will be added to this repository when it is ready.

---

## Test the API with Postman

**Postman** is used to check the API without writing a frontend.

**Setup:**
1. Install Postman (desktop app or web).
2. Start the API (Phase 1: `python phase1.py` | Phase 2: `docker compose up`).
3. Base URL: `http://127.0.0.1:5000` (Phase 1) or `http://localhost:5000` (Phase 2).

**Examples:**

| Action | Method | URL | Body (JSON) |
|--------|--------|-----|-------------|
| Hello | GET | `/` | none |
| List users | GET | `/users` | none |
| Add user (Phase 1) | POST | `/users` | `{"name": "Anna"}` |
| Add user (Phase 2) | POST | `/users` | `{"name": "Anna", "email": "anna@mail.com"}` |
| Login (Phase 2) | POST | `/users/login` | `{"email": "abc@123", "password": "123"}` |

For **Phase 2 profile** (`GET /users/profile`):
1. Call `/users/login` and copy `access_token` from the response.
2. Open the **Authorization** tab, choose **Bearer Token**, paste the token.
3. Send `GET` to `/users/profile`.

Check status code and JSON body in Postman after each request.

---

## Requirements (general)

- Python 3.10+ (for local run)
- Docker Desktop (for Phase 2)
- Postman (recommended for API testing)
- Basic knowledge of HTTP and JSON

