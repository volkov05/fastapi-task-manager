# 🚀 FastAPI Task Manager

Асинхронный backend для управления задачами, построенный на FastAPI.

## ⚙️ Технологии

* FastAPI
* SQLAlchemy (async)
* PostgreSQL
* Alembic (миграции)
* Docker & Docker Compose
* JWT Authentication
* Pydantic

## 📦 Возможности

* Регистрация и авторизация пользователей
* CRUD для задач
* Асинхронная работа с базой данных
* Миграции базы данных
* Контейнеризация через Docker

## 🐳 Запуск через Docker

```bash
docker compose up --build
```

Приложение будет доступно:

* API: http://localhost:8000
* Docs: http://localhost:8000/docs

---

## 🛠️ Code Quality

```bash
black .
mypy .
pylint app
```

---

## 📂 Структура проекта

```
app/
 ├── routers/
 ├── models/
 ├── schemas/
 ├── crud/
 ├── database.py
 └── main.py
```

---

## 🔐 Переменные окружения (.env)

```
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASS=0000
DB_NAME=task_app_DB
SECRET_KEY=your_secret_key
```

---

## 📌 Планы по развитию

* Написание тестов (pytest, pytest-asyncio)
* Redis + Celery (фоновые задачи)
* CI/CD (GitLab CI)
* Кэширование
* Роли пользователей

---

## 👨‍💻 Автор

Artur Volkov
