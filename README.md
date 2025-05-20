# FastAPI Todo App

Проект управления задачами на FastAPI с тестами

## Отчет о покрытии тестами
[Посмотреть детальный отчет](docs/coverage/index.html)

## Запуск проекта
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
uvicorn src.main:app --reload
```

## Запуск тестов
```bash
# Все тесты
pytest 

# Подробный вывод тестов
pytest -v

# Генерация HTML-отчета
pytest --cov=src --cov-report=html

# Нагрузочное тестирование
locust -f tests/locustfile.py
```

## Структура проекта
```
FastAPI-tests/
├── src/                       
│   ├── __init__.py            # Инициализация пакета
│   ├── main.py                # Точка входа FastAPI
│   ├── models.py              # Модели SQLAlchemy
│   ├── schemas.py             # Pydantic схемы
│   ├── CRUD.py                # Операции с базой данных
│   ├── database.py            # Настройки подключения к БД
│   └── dependencies.py        # Зависимости приложения
│
├── tests/                     # Тесты
│   │    
│   ├── test_models.py
│   ├── test_schemas.py
│   ├── test_crud.py
│   ├── test_api.py
│   ├── test_errors.py
│   │
│   ├── conftest.py            # Фикстуры pytest
│   └── locustfile.py          # Нагрузочное тестирование
│
├── alembic/                   # Миграции базы данных
│   ├── env.py
│   └── script.py.mako
│
├── .gitignore                 # Игнорируемые файлы
├── pytest.ini                 # Конфигурация pytest
├── requirements.txt           # Зависимости Python
└── README.md                  # Этот файл
```