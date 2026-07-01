# Course Management API

A production-quality **Django REST Framework** project for managing academic
departments, students, courses, and enrollments. Built to demonstrate
function-based views, class-based views, viewsets, routers, custom actions,
validation, and testing.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [Django Admin](#django-admin)
- [API Documentation](#api-documentation)
- [Custom Action](#custom-action)
- [Validation Rules](#validation-rules)
- [Testing](#testing)
- [Postman Collection](#postman-collection)
- [Screenshots](#screenshots)

---

## Tech Stack

- Python 3.12
- Django 5.x
- Django REST Framework
- SQLite (default database)
- Postman (API testing collection included)

---

## Project Structure

```
CourseManagementAPI/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                 # sample pre-populated database
├── .gitignore
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── courses/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── tests.py
│   ├── signals.py
│   ├── validators.py
│   ├── utils.py
│   └── migrations/
├── templates/
├── static/
├── media/
├── postman/
│   └── CourseManagement.postman_collection.json
└── screenshots/
```

---

## Installation

### 1. Clone / extract the project

```bash
cd CourseManagementAPI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup

The project ships with a pre-populated `db.sqlite3` sample database
(2 departments, 2 students, 3 courses, 3 enrollments) so you can start
testing immediately. To reset or rebuild it from scratch:

```bash
# Remove the sample database (optional)
rm db.sqlite3

# Generate migrations (already included, but safe to re-run)
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Create a superuser (for Django Admin access)

```bash
python manage.py createsuperuser
```

> The included sample database already has a superuser:
> **username:** `admin` **password:** `admin12345`
> (Change this immediately if deploying anywhere public.)

---

## Running the Server

```bash
python manage.py runserver
```

The API will be available at: **http://127.0.0.1:8000/api/**
The Django Admin will be available at: **http://127.0.0.1:8000/admin/**

---

## Django Admin

All four models are registered with:

- Readable `list_display` columns
- `search_fields` (e.g. search students by name/email, courses by code/title)
- `list_filter` (e.g. filter students by department, courses by credits)
- Sensible default `ordering`

---

## API Documentation

Base URL: `/api/`

### Production Endpoints (ViewSets + DefaultRouter)

| Method | Endpoint                          | Description                              |
|--------|------------------------------------|-------------------------------------------|
| GET    | `/api/departments/`                | List all departments                     |
| POST   | `/api/departments/`                | Create a department                      |
| GET    | `/api/departments/<id>/`           | Retrieve a department                    |
| PUT    | `/api/departments/<id>/`           | Update a department                      |
| DELETE | `/api/departments/<id>/`           | Delete a department                      |
| GET    | `/api/departments/<id>/courses/`   | List courses in a department (custom)    |
| GET    | `/api/departments/<id>/students/`  | List students in a department (custom)   |
| GET    | `/api/students/`                   | List all students                        |
| POST   | `/api/students/`                   | Create a student                         |
| GET    | `/api/students/<id>/`              | Retrieve a student                       |
| PUT    | `/api/students/<id>/`              | Update a student                         |
| DELETE | `/api/students/<id>/`              | Delete a student                         |
| GET    | `/api/students/<id>/courses/`      | List courses a student is enrolled in    |
| GET    | `/api/courses/`                    | List all courses                         |
| POST   | `/api/courses/`                    | Create a course                          |
| GET    | `/api/courses/<id>/`               | Retrieve a course                        |
| PUT    | `/api/courses/<id>/`               | Update a course                          |
| DELETE | `/api/courses/<id>/`               | Delete a course                          |
| GET    | `/api/courses/<id>/students/`      | **Custom action** — students enrolled in this course |
| GET    | `/api/enrollments/`                | List all enrollments                     |
| POST   | `/api/enrollments/`                | Create an enrollment                     |
| GET    | `/api/enrollments/<id>/`           | Retrieve an enrollment                   |
| DELETE | `/api/enrollments/<id>/`           | Delete an enrollment                     |

### Demonstration Endpoints

**Part 1 — Function-Based Views (Department)**

| Method | Endpoint                            |
|--------|---------------------------------------|
| GET/POST | `/api/fbv/departments/`             |
| GET/PUT/DELETE | `/api/fbv/departments/<id>/`   |

**Part 2 — Class-Based Views (Student)**

| Method | Endpoint                                      |
|--------|------------------------------------------------|
| GET/POST | `/api/cbv/students/` (`APIView`)              |
| GET/POST | `/api/cbv/students/generic/` (`ListCreateAPIView`) |
| GET/PUT/PATCH/DELETE | `/api/cbv/students/generic/<id>/` (`RetrieveUpdateDestroyAPIView`) |

### Example JSON

**Create a Department**
```json
POST /api/departments/
{
  "name": "Computer Science",
  "description": "Department of Computer Science"
}
```

**Create a Student**
```json
POST /api/students/
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "phone": "1234567890",
  "department": 1
}
```

**Create a Course**
```json
POST /api/courses/
{
  "title": "Intro to Programming",
  "code": "CS101",
  "credits": 4,
  "department": 1
}
```

**Create an Enrollment**
```json
POST /api/enrollments/
{
  "student": 1,
  "course": 1
}
```

**Error response format** (400/404 etc.):
```json
{
  "error": true,
  "status_code": 400,
  "details": {
    "code": ["Course with this code already exists."]
  }
}
```

---

## Custom Action

`GET /api/courses/<id>/students/` uses DRF's `@action(detail=True)` decorator
on `CourseViewSet` to return **only the students enrolled in that specific
course** — not the full student list. Similar bonus actions are provided:

- `GET /api/departments/<id>/courses/`
- `GET /api/departments/<id>/students/`
- `GET /api/students/<id>/courses/`

---

## Validation Rules

| Rule                                   | Where enforced                          |
|-----------------------------------------|------------------------------------------|
| Unique student email                   | `StudentSerializer.validate_email`      |
| Unique course code (format: `AB123`)   | `CourseSerializer.validate_code` + model validator |
| No duplicate enrollment (same student + course) | `EnrollmentSerializer.validate` + DB `UniqueConstraint` |
| Credits must be 1–10                   | `CourseSerializer.validate_credits` + model validators |
| Missing required fields → 400          | DRF serializer `required` fields        |
| Invalid/non-existent related IDs → 400 | DRF `PrimaryKeyRelatedField`            |
| Non-existent object → 404              | `get_object_or_404` / DRF `get_object`  |

---

## Testing

Run the full test suite (39 tests covering models, serializers, CRUD,
validation, custom actions, and 400/404 handling):

```bash
python manage.py test courses
```

Verbose output:

```bash
python manage.py test courses -v 2
```

---

## Postman Collection

Import [`postman/CourseManagement.postman_collection.json`](postman/CourseManagement.postman_collection.json)
into Postman. It includes requests for every endpoint above, organized into
folders: Departments, Students, Courses, Enrollments, Part 1 (FBV), and
Part 2 (CBV). A `base_url` collection variable defaults to
`http://127.0.0.1:8000/api`.

---

## Screenshots

Place your Postman/browser testing screenshots inside the `screenshots/`
folder to document verified requests (list, create, update, delete, and the
custom `/courses/<id>/students/` action).

---

## License

This project was generated for educational purposes as part of a Django
REST Framework hands-on exercise (Digital Nurture 5.0).
