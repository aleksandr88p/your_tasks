# YourTasks API

[English](#english) | [Русский](#русский)

---

## Русский

### 📋 О проекте

**YourTasks API** — это REST API для системы управления задачами и логирования времени. Проект разработан как бэкенд для Telegram-бота, который позволяет пользователям создавать задачи и вручную логировать потраченное на них время.

**Основной сценарий использования:**
- Пользователь создает задачу через Telegram-бота (например: "Гитара")
- Пользователь добавляет потраченное время (например: "+2 часа к задаче 'Гитара'")
- Пользователь просматривает статистику по задачам и времени

### 🚀 Функционал (MVP)

#### Управление задачами
- ✅ Создание новой задачи
- ✅ Получение списка всех задач пользователя
- ✅ Получение конкретной задачи по ID
- ✅ Изменение статуса задачи (active/completed)

#### Логирование времени
- ✅ Добавление потраченного времени к задаче
- ✅ Получение всех логов времени пользователя
- ✅ Получение логов времени по конкретной задаче

#### Статистика
- ✅ Общая статистика пользователя (общее время, количество задач)
- ✅ Статистика по конкретной задаче

### 🛠 Технологический стек

- **Python 3.12+** - основной язык
- **FastAPI** - веб-фреймворк для REST API
- **SQLAlchemy 2.0 (Async)** - ORM для работы с базой данных
- **Supabase (PostgreSQL)** - удаленная база данных
- **Pydantic v2** - валидация данных и схемы
- **asyncpg** - асинхронный драйвер PostgreSQL
- **python-dotenv** - управление переменными окружения

### 📁 Структура проекта

```
app/
├── core/           # Конфигурация и работа с БД
│   ├── config.py   # Настройки подключения к Supabase
│   └── database.py # SQLAlchemy engine и сессии
├── models/         # SQLAlchemy модели
│   ├── base.py     # Базовый класс
│   ├── user.py     # Модель пользователя
│   ├── task.py     # Модель задачи
│   └── timelog.py  # Модель лога времени
├── routers/        # FastAPI роутеры (эндпоинты)
│   ├── tasks.py    # Управление задачами
│   ├── timelogs.py # Логирование времени
│   └── stats.py    # Статистика
├── schemas/        # Pydantic схемы
│   ├── task.py     # Схемы задач
│   ├── timelog.py  # Схемы логов
│   └── stats.py    # Схемы статистики
└── main.py         # Точка входа FastAPI
```

### 🏗 Архитектура

**Принципы:**
- **Модульность** - четкое разделение ответственности
- **Асинхронность** - все операции с БД асинхронные
- **Type Safety** - строгая типизация везде
- **Clean Code** - простые и понятные решения

**Поток данных:**
1. Telegram-бот → HTTP запрос с `telegram_user_id` в хедере
2. FastAPI получает пользователя по `telegram_id` или создает нового
3. Все SQL запросы используют внутренний `user.id` для фильтрации
4. Ответ возвращается в JSON формате

### 🚀 Быстрый старт

#### 1. Клонирование и установка
```bash
git clone <repository-url>
cd your_tasks
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate для Windows
pip install -r requirements.txt
```

#### 2. Настройка Supabase
1. Создайте проект в [Supabase](https://supabase.com)
2. В настройках проекта найдите данные подключения:
   - Host: `db.xxx.supabase.co`
   - Port: `5432`
   - User: `postgres`
   - Password: `<your-password>`
   - Database: `postgres`

#### 3. Конфигурация
Создайте файл `.env`:
```env
user=postgres
password=your_supabase_password
host=db.your_project.supabase.co
port=5432
dbname=postgres
```

#### 4. Запуск
```bash
uvicorn app.main:app --reload
```

API будет доступен по адресу: `http://localhost:8000`

### 📚 Документация API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 🔑 Аутентификация

Аутентификация происходит через `telegram_user_id` в HTTP хедере:
```
telegram_user_id: 12345
```

### 📝 Примеры запросов

#### Создание задачи
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "telegram_user_id: 12345" \
  -H "Content-Type: application/json" \
  -d '{"title": "Изучить FastAPI"}'
```

#### Добавление времени
```bash
curl -X POST "http://localhost:8000/timelogs" \
  -H "telegram_user_id: 12345" \
  -H "Content-Type: application/json" \
  -d '{"task_id": 1, "minutes": 120, "comment": "Читал документацию"}'
```

#### Получение статистики
```bash
curl -X GET "http://localhost:8000/stats/summary" \
  -H "telegram_user_id: 12345"
```

### 🔧 Разработка

#### Локальная разработка с SQLite
Для локальной разработки можно использовать SQLite:
```env
DATABASE_URL=sqlite+aiosqlite:///./your_tasks.db
```

#### Тестирование подключения
```bash
python test_async_conn_v2.py
```

### 📋 Эндпоинты

#### Tasks
- `POST /tasks` - Создать задачу
- `GET /tasks` - Получить задачи пользователя
- `GET /tasks/{task_id}` - Получить конкретную задачу
- `PATCH /tasks/{task_id}/status` - Изменить статус задачи

#### TimeLogs
- `POST /timelogs` - Добавить время к задаче
- `GET /timelogs` - Получить все логи времени
- `GET /timelogs/task/{task_id}` - Получить логи по задаче

#### Stats
- `GET /stats/summary` - Общая статистика
- `GET /stats/tasks/{task_id}` - Статистика по задаче

### 🤝 Интеграция с Telegram-ботом

Пример кода для интеграции:
```python
import requests

# Создание задачи
def create_task(telegram_id: int, title: str):
    headers = {"telegram_user_id": str(telegram_id)}
    data = {"title": title}
    response = requests.post("http://your-api.com/tasks", headers=headers, json=data)
    return response.json()

# Добавление времени
def add_time(telegram_id: int, task_id: int, minutes: int, comment: str):
    headers = {"telegram_user_id": str(telegram_id)}
    data = {"task_id": task_id, "minutes": minutes, "comment": comment}
    response = requests.post("http://your-api.com/timelogs", headers=headers, json=data)
    return response.json()
```

---

## English

### 📋 About Project

**YourTasks API** is a REST API for task management and time logging system. The project is developed as a backend for a Telegram bot that allows users to create tasks and manually log time spent on them.

**Main usage scenario:**
- User creates a task via Telegram bot (e.g., "Guitar")
- User adds spent time (e.g., "+2 hours to task 'Guitar'")
- User views statistics on tasks and time

### 🚀 Features (MVP)

#### Task Management
- ✅ Create new task
- ✅ Get all user tasks
- ✅ Get specific task by ID
- ✅ Change task status (active/completed)

#### Time Logging
- ✅ Add spent time to task
- ✅ Get all user time logs
- ✅ Get time logs for specific task

#### Statistics
- ✅ User summary statistics (total time, task count)
- ✅ Specific task statistics

### 🛠 Tech Stack

- **Python 3.12+** - main language
- **FastAPI** - web framework for REST API
- **SQLAlchemy 2.0 (Async)** - ORM for database operations
- **Supabase (PostgreSQL)** - remote database
- **Pydantic v2** - data validation and schemas
- **asyncpg** - async PostgreSQL driver
- **python-dotenv** - environment variables management

### 📁 Project Structure

```
app/
├── core/           # Configuration and database operations
│   ├── config.py   # Supabase connection settings
│   └── database.py # SQLAlchemy engine and sessions
├── models/         # SQLAlchemy models
│   ├── base.py     # Base class
│   ├── user.py     # User model
│   ├── task.py     # Task model
│   └── timelog.py  # Time log model
├── routers/        # FastAPI routers (endpoints)
│   ├── tasks.py    # Task management
│   ├── timelogs.py # Time logging
│   └── stats.py    # Statistics
├── schemas/        # Pydantic schemas
│   ├── task.py     # Task schemas
│   ├── timelog.py  # Time log schemas
│   └── stats.py    # Statistics schemas
└── main.py         # FastAPI entry point
```

### 🏗 Architecture

**Principles:**
- **Modularity** - clear separation of responsibilities
- **Asynchronous** - all database operations are async
- **Type Safety** - strict typing everywhere
- **Clean Code** - simple and understandable solutions

**Data Flow:**
1. Telegram bot → HTTP request with `telegram_user_id` in header
2. FastAPI gets user by `telegram_id` or creates new one
3. All SQL queries use internal `user.id` for filtering
4. Response returned in JSON format

### 🚀 Quick Start

#### 1. Clone and Install
```bash
git clone <repository-url>
cd your_tasks
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate for Windows
pip install -r requirements.txt
```

#### 2. Setup Supabase
1. Create project at [Supabase](https://supabase.com)
2. In project settings find connection data:
   - Host: `db.xxx.supabase.co`
   - Port: `5432`
   - User: `postgres`
   - Password: `<your-password>`
   - Database: `postgres`

#### 3. Configuration
Create `.env` file:
```env
user=postgres
password=your_supabase_password
host=db.your_project.supabase.co
port=5432
dbname=postgres
```

#### 4. Run
```bash
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`

### 📚 API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 🔑 Authentication

Authentication via `telegram_user_id` in HTTP header:
```
telegram_user_id: 12345
```

### 📝 Request Examples

#### Create Task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "telegram_user_id: 12345" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI"}'
```

#### Add Time
```bash
curl -X POST "http://localhost:8000/timelogs" \
  -H "telegram_user_id: 12345" \
  -H "Content-Type: application/json" \
  -d '{"task_id": 1, "minutes": 120, "comment": "Read documentation"}'
```

#### Get Statistics
```bash
curl -X GET "http://localhost:8000/stats/summary" \
  -H "telegram_user_id: 12345"
```

### 🔧 Development

#### Local Development with SQLite
For local development you can use SQLite:
```env
DATABASE_URL=sqlite+aiosqlite:///./your_tasks.db
```

#### Test Connection
```bash
python test_async_conn_v2.py
```

### 📋 Endpoints

#### Tasks
- `POST /tasks` - Create task
- `GET /tasks` - Get user tasks
- `GET /tasks/{task_id}` - Get specific task
- `PATCH /tasks/{task_id}/status` - Update task status

#### TimeLogs
- `POST /timelogs` - Add time to task
- `GET /timelogs` - Get all time logs
- `GET /timelogs/task/{task_id}` - Get task time logs

#### Stats
- `GET /stats/summary` - Summary statistics
- `GET /stats/tasks/{task_id}` - Task statistics

### 🤝 Telegram Bot Integration

Integration code example:
```python
import requests

# Create task
def create_task(telegram_id: int, title: str):
    headers = {"telegram_user_id": str(telegram_id)}
    data = {"title": title}
    response = requests.post("http://your-api.com/tasks", headers=headers, json=data)
    return response.json()

# Add time
def add_time(telegram_id: int, task_id: int, minutes: int, comment: str):
    headers = {"telegram_user_id": str(telegram_id)}
    data = {"task_id": task_id, "minutes": minutes, "comment": comment}
    response = requests.post("http://your-api.com/timelogs", headers=headers, json=data)
    return response.json()
```

---

## 📄 License

MIT License - feel free to use this project for your own purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Contact

If you have any questions, feel free to open an issue in this repository.
