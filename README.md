# Recipe App API

Backend REST API built with **Django** and **Django REST Framework**, developed following a Test-Driven Development (TDD) approach. Users can register, authenticate, and manage their own recipes, including tags, ingredients, and images.

## Features

- Custom user model with token-based authentication
- Full CRUD for recipes (create, list, retrieve, update, delete)
- Filter recipes by tags and ingredients
- Upload and manage recipe images
- Auto-generated API documentation with drf-spectacular (Swagger UI)
- Dockerized development environment with PostgreSQL
- Automated testing and linting via GitHub Actions CI

## Tech Stack

- Python / Django 6
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- drf-spectacular (OpenAPI schema & Swagger UI)
- Pillow (image handling)
- Flake8 (linting)
- GitHub Actions (CI/CD)

## Getting Started

### Prerequisites

- Docker and Docker Compose installed

### Run the project

```bash
docker compose up
```

The API will be available at `http://127.0.0.1:8000`.

### Run the tests

```bash
docker compose run --rm app sh -c "python manage.py test"
```

### Run the linter

```bash
docker compose run --rm app sh -c "flake8"
```

## API Documentation

Once the project is running, interactive API docs are available at:

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema`

## Main Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/user/create/` | Register a new user |
| POST | `/api/user/token/` | Obtain an auth token |
| GET/PUT/PATCH | `/api/user/me/` | Retrieve or update the authenticated user |
| GET/POST | `/api/recipe/recipes/` | List or create recipes |
| GET/PUT/PATCH/DELETE | `/api/recipe/recipes/{id}/` | Retrieve, update, or delete a recipe |
| POST | `/api/recipe/recipes/{id}/upload-image/` | Upload an image for a recipe |
| GET | `/api/recipe/tags/` | List tags |
| GET | `/api/recipe/ingredients/` | List ingredients |

All recipe endpoints require authentication and only return data belonging to the authenticated user.

## Project Status

Built as part of a hands-on backend development learning, applying Django REST Framework architecture (serializers, viewsets, routers), Docker-based workflows, and CI pipelines.

## About

Developed by [Victor Tapia](https://github.com/Victoorto) as a backend development project.
