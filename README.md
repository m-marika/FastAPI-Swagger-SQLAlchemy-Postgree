# FastAPI + Swagger + SQAlchemy

Тестовое задание

## Локальное развёртывание

1. Установите python или настройте виртуальную среду
2. Выполните установку зависимостей

   ```pip install -r requirements-dev.txt```
3. Выполните настройку и миграцию БД
   config.py:
      DATABASE_URL: str = "postgresql://<username>:<password>@localhost/<your_BD_name>"

   ```alembic init -t async migration```
   ```alembic revision --autogenerate -m "Initial revision```
   ```alembic upgrade head```

### Запуск

Выполните команду `uvicorn app.main:app --reload`

По умолчанию приложение запустится на 8000-м порту и использованием sqlite (строку подключения можно поменять с помощью
переменных окружения - .env)

- http://localhost:8000
- http://127.0.0.1:8000/docs#/

## Запуск с помощью docker-compose

Выполнить команды:
 ```docker build -t fastapi-app .```
 ```docker-compose up -d```

При запуске контейнера приложения будут установлены все неустановленные зависимости 

По умолчанию приложение запустится на 8000-м порту и использованием postgres 

- http://localhost:8000
- http://localhost:8000/docs#/


