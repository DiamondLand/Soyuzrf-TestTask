# Task Management API
## Описание
Этот проект представляет собой RESTful API для управления задачами, разработанный на FastAPI с использованием PostgreSQL и SQLAlchemy. API поддерживает аутентификацию через JWT, CRUD-операции с задачами, аналитику, WebSocket (и telegram) уведомления, а также экспорт данных в CSV.
## 🚀 Запуск проекта
**1. Установка зависимостей**
Перед запуском убедитесь, что у вас установлен Python 3.10+ и установлен pip.
> pip install -r requirements.txt

**2. Настройка конфига**
- Выбрать `MODE` В `backend/core/config.py` и там же настроить подключение к базе данных.
- Указать в `TG_TOKEN` токен Telegram-бота для отбивки уведомлений
- Указать в `TG_ID` id того, кому присылать уведомления об изменениях таска.

**3. Запуск приложения**
Перейти в `backend/cli.py` и запустить его.

**4. Документация API**
После запуска проекта можно будет перейти в документации.
Swagger UI: http://127.0.0.1:9000/docs
Redoc: http://127.0.0.1:9000/redoc

## 😎 Postman-коллекция
Находится в файле `postman_collection.json`, в корневой директории.

## 🎇 Тестирование
Всё необходимое для тестов, написанных на `pytest` размещено в`backend/tests`. Кофиг тестов - `backend/tests/conftest.py`

## ✨ Архитектура
- Роутеры вынесены в `backend/api/` и инициализированы в `backend/api/__init__.py`
- Сервисы вынесены в `backend/service/` и импортируются в `backend/api/`.
- Схемы вынесены в `backend/schema/`.
- Создана папка `backend/utils/` для хранения в ней дополнительных файлов: `HTTPException's`, `jwt-security`, `dependencies`.
- Написан логгер, собирающий данные о запросах в json-формате:
```
{
    "timestamp": "2025-03-11 | 10:56:33.134386",
    "level": "INFO",
    "message": "[ET] Request: /openapi.json, Execution Time: 0.006 seconds",
    "module": "middleware",
    "funcName": "dispatch",
    "path": "/openapi.json",
    "execution_time": 0.006,
    "method": "GET",
    "remote_addr": "127.0.0.1",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
},
{
    "timestamp": "2025-03-11 | 10:56:39.157302",
    "level": "INFO",
    "message": "[ET] Request: /api/v1/tasks/, Execution Time: 0.01 seconds",
    "module": "middleware",
    "funcName": "dispatch",
    "path": "/api/v1/tasks/",
    "execution_time": 0.0103,
    "method": "GET",
    "remote_addr": "127.0.0.1",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
},
```
## Архитектурное древо:
```
📦 backend
 ┣ 📂 api
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 analytics.py
 ┃ ┣ 📜 auth.py
 ┃ ┗ 📜 tasks.py
 ┣ 📂 core
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 config.py
 ┃ ┗ 📜 lifespan.py
 ┣ 📂 database
 ┃ ┣ 📜 __init__.py
 ┃ ┗ 📜 models.py
 ┣ 📂 logs
 ┃ ┣ 📜 10-03-2025_log.json
 ┃ ┗ 📜 11-03-2025_log.json
 ┣ 📂 schema
 ┃ ┣ 📜 auth_schema.py
 ┃ ┗ 📜 task_schema.py
 ┣ 📂 service
 ┃ ┣ 📜 analytics_service.py
 ┃ ┣ 📜 auth_service.py
 ┃ ┗ 📜 task_service.py
 ┣ 📂 tests
 ┃ ┣ 📜 conftest.py
 ┃ ┣ 📜 test_auth.py
 ┃ ┗ 📜 test_tasks.py
 ┣ 📂 utils
 ┃ ┣ 📜 dependencies.py
 ┃ ┣ 📜 exception.py
 ┃ ┣ 📜 security.py
 ┣ 📜 cli.py
 ┣ 📜 middleware.py
 ┗ 📜 my_logger.py
```
