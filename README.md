# Test Project

Это тестовый проект, предназначенный для демонстрации базовой функциональности приложения на Python. Проект включает базовую настройку и тестирование с использованием Docker и Poetry для управления зависимостями.

## Предварительные требования

- Docker
- Python 3.8+
- Poetry
- PostgreSQL (или любая другая используемая СУБД)

## Структура проекта

- `main.py`: Точка входа для приложения.
- `models.py`: Содержит модели данных.
- `main_test.py`: Содержит основные тесты для приложения.
- `test.py`: Дополнительные тесты.
- `Dockerfile`: Конфигурация Docker для контейнеризации приложения.
- `pyproject.toml`: Конфигурация для управления зависимостями с помощью Poetry.
- `poetry.lock`: Файл блокировки зависимостей Poetry.

## Настройка

### Создание баз данных

1. Создайте две отдельные базы данных:
    ```sql
    CREATE DATABASE database1;
    CREATE DATABASE database2;
    ```

2. Создайте пользователя и наделите его правами на обе базы данных:
    ```sql
    CREATE USER your_user WITH PASSWORD 'your_password';
    GRANT ALL PRIVILEGES ON DATABASE database1 TO your_user;
    GRANT ALL PRIVILEGES ON DATABASE database2 TO your_user;
    ```

### Использование Docker

1. Постройте Docker-образ:
    ```bash
    docker build -t test_project .
    ```

2. Запустите Docker-контейнер:
    ```bash
    docker run -it --rm test_project
    ```

### Использование Poetry

1. Установите Poetry:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. Установите зависимости:
    ```bash
    poetry install
    ```

3. Запустите приложение:
    ```bash
    poetry run python main.py
    ```

## Запуск тестов

### Использование Docker

1. Постройте Docker-образ (если не сделано ранее):
    ```bash
    docker build -t test_project .
    ```

2. Запустите тесты внутри Docker-контейнера:
    ```bash
    docker run -it --rm test_project pytest
    ```

### Использование Poetry

1. Запустите тесты:
    ```bash
    poetry run pytest
    ```

## Использование Docker Compose

1. Создайте и запустите контейнеры с помощью Docker Compose:
    ```bash
    docker-compose up --build
    ```

2. Чтобы запустить контейнеры в фоновом режиме:
    ```bash
    docker-compose up -d --build
    ```
