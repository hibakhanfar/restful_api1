# Restful API Task — Django REST Framework

A backend project built with Django and Django REST Framework that implements user registration, JWT-based login, and management of two types of resources:
- **Profile** (a user-bound resource — each user only sees/edits their own)
- **Announcement** (a shared authenticated resource — visible to all logged-in users)

---

##  Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Programming language |
| Django 6.1 | Core framework |
| Django REST Framework | Building the API |
| djangorestframework-simplejwt | JWT authentication (Access / Refresh tokens) |
| PostgreSQL (psycopg2-binary) | Database |
| python-dotenv | Loading environment variables from `.env` |
| uv | Package & virtual environment management |
| pre-commit | Code checks before each commit |

---

## Project Structure

```
restful-api-task/
│
├── manage.py
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── authentication/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── announcements/
│       ├── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
```

###  Why this structure?
The project follows an **app-per-responsibility** pattern instead of putting everything in one big app:
- `accounts` → handles user identity and personal data (User + Profile).
- `authentication` → handles only the auth flow (login/register).
- `announcements` → handles the resource shared between all users.

This separation keeps each app independent and easier to extend or test on its own — a common pattern (modular apps) in larger Django projects.

---

## Authentication

The project uses **JWT (JSON Web Token)** via `djangorestframework-simplejwt`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

After logging in, you receive an `access` and a `refresh` token. Send the access token with every protected request like this:

```
Authorization: Bearer <access_token>
```

---

##  Database Models

### User (`apps/accounts/models.py`)
A custom User model that extends `AbstractUser`, using **email** as the `USERNAME_FIELD` instead of username.

### Profile (`apps/accounts/models.py`)
```
user          → OneToOneField(User, on_delete=CASCADE)
bio           → TextField (optional)
avatar_url    → URLField (optional)
created_at    → DateTimeField (auto_now_add)
```
Automatically created for every new user inside `RegisterSerializer.create()`.

### Announcement (`apps/announcements/models.py`)
```
author        → ForeignKey(User, on_delete=CASCADE)
title         → CharField(max_length=200)
content       → TextField
created_at    → DateTimeField (auto_now_add)
```
The `author` field is `read_only` in the serializer and is set automatically from `request.user` inside the view.

---

## Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/register/` | Public | Registers a new user and creates their profile automatically |
| POST | `/api/login/` | Public | Authenticates credentials and returns Access / Refresh tokens |
| POST | `/api/token/refresh/` | Public | Refreshes the Access Token using the Refresh Token |
| GET | `/api/profile/` | Authenticated | Returns only the current authenticated user's profile |
| PATCH | `/api/profile/` | Authenticated | Updates the current authenticated user's profile |
| GET | `/api/announcement/` | Authenticated | Lists all announcements from every user |
| POST | `/api/announcement/` | Authenticated | Creates a new announcement (author = current user) |


---

### 2. Create a `.env` file in the project root
```env
SECRET_KEY=your-secret-key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 3. Apply migrations
```bash
python manage.py migrate
```

### 4. Run the server
```bash
python manage.py runserver
```
