# Flowers Microservice

Микросервис для работы с цветами: создание, получение, фильтрация и обновление информации о букетах и категориях. Реализован с использованием FastAPI и PostgreSQL.

---

## Стек технологий

- Python 3.11
- FastAPI
- PostgreSQL
- Docker & Docker Compose
- Pydantic для валидации данных

---

## Функционал API

| Эндпоинт                   | Метод | Описание                                      |
|-----------------------------|-------|----------------------------------------------|
| `/flowers/`                 | GET   | Получение всех букетов                        |
| `/flowers/filters/`         | POST  | Получение букетов по фильтрам (цены, цветы) |
| `/flowers/{f_id}`           | GET   | Получение конкретного букета по ID           |
| `/flowers/`                 | POST  | Добавление нового букета с компонентами      |
| `/flowers/category`         | POST  | Добавление новой категории цветов            |
| `/flowers/description/{id}` | PUT   | Обновление описания букета по ID             |


Запуск проекта

Клонируйте репозиторий:

git clone https://github.com/lisssaiiik/flower-service.git
cd flower-service

Запустите сервисы через Docker Compose:

docker-compose up --build

После запуска микросервис будет доступен по адресу:

http://localhost:8000
