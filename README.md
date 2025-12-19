# MVP Регистрации Пользователей

Полноценный минимально жизнеспособный продукт (MVP), реализующий систему регистрации пользователей с современной full-stack архитектурой.

## Архитектура

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI (Python)
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker Compose

## Структура проекта

```
project/
 ├── frontend/
 │   ├── src/
 │   │   ├── App.tsx
 │   │   ├── api.ts
 │   │   ├── RegisterForm.tsx
 │   │   └── main.tsx
 │   ├── package.json
 │   ├── tsconfig.json
 │   ├── vite.config.ts
 │   ├── index.html
 │   └── Dockerfile
 ├── backend/
 │   ├── main.py
 │   ├── models.py
 │   ├── database.py
 │   ├── schemas.py
 │   ├── config.py
 │   ├── utils.py
 │   ├── routes/
 │   │   └── auth.py
 │   ├── tests/
 │   │   └── test_register.py
 │   ├── requirements.txt
 │   └── Dockerfile
 ├── docker-compose.yml
 ├── .env
 ├── .env.example
 └── README.md
```

## Быстрый старт

### Требования

- Установленные Docker и Docker Compose
- Git (опционально, для клонирования)

### Запуск приложения

1. **Клонируйте или перейдите в директорию проекта**

2. **Запустите все сервисы одной командой:**

```bash
docker compose up --build
```

Эта команда:
- Соберет контейнеры frontend, backend и базы данных
- Запустит PostgreSQL базу данных
- Запустит FastAPI backend на порту 8000
- Запустит React frontend на порту 5173
- Настроит сетевые соединения между сервисами

3. **Откройте приложение:**

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Документация API**: http://localhost:8000/docs (Swagger UI)
- **Альтернативная документация API**: http://localhost:8000/redoc

### Остановка приложения

```bash
docker compose down
```

Для удаления volumes (данных базы данных):

```bash
docker compose down -v
```

## API Endpoints

### POST /api/register

Регистрация нового пользователя.

**Тело запроса:**
```json
{
  "login": "user123",
  "password": "Password123!"
}
```

**Правила валидации:**
- `login`: 3-32 символа, только буквы, цифры, точки, подчеркивания или дефисы
- `password`: Минимум 8 символов, должен содержать:
  - Хотя бы одну заглавную букву
  - Хотя бы одну строчную букву
  - Хотя бы одну цифру
  - Хотя бы один специальный символ

**Ответы:**

- **201 Created**: Успех
  ```json
  {
    "message": "user created"
  }
  ```

- **422 Unprocessable Entity**: Ошибка валидации
  ```json
  {
    "detail": "Password must contain at least one uppercase letter"
  }
  ```

- **409 Conflict**: Дублирующийся логин
  ```json
  {
    "detail": "Login already exists"
  }
  ```

## Примеры использования

### Использование curl

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"login":"testuser","password":"Password123!"}'
```

### Использование Frontend

1. Откройте http://localhost:5173 в браузере
2. Заполните форму регистрации:
   - **Логин**: Введите имя пользователя (3-32 символа, буквы/цифры/._-)
   - **Пароль**: Введите надежный пароль (мин. 8 символов с заглавной, строчной буквой, цифрой и спецсимволом)
3. Нажмите "Зарегистрироваться"
4. При успехе вы увидите сообщение "user created"
5. При ошибке будут отображены сообщения валидации

## Тестирование

### Запуск тестов Backend

```bash
# Войдите в контейнер backend
docker compose exec backend bash

# Запустите тесты
pytest tests/ -v
```

Или запустите тесты напрямую:

```bash
docker compose exec backend pytest tests/ -v
```

### Покрытие тестами

Набор тестов включает:

1. **test_register_success**: Тестирует успешную регистрацию пользователя
2. **test_register_duplicate_login**: Тестирует ошибку 409 при дублирующемся логине
3. **test_weak_password**: Тестирует ошибку 422 при слабом пароле

## Переменные окружения

Приложение использует переменные окружения, определенные в файле `.env`. См. `.env.example` для справки.

### Переменные Backend

- `DATABASE_URL`: Строка подключения к PostgreSQL
- `HASH_SCHEME`: Схема хеширования паролей (argon2)
- `SECRET_KEY`: Секретный ключ приложения
- `APP_ENV`: Окружение (development/production)
- `PORT`: Порт backend (по умолчанию: 8000)
- `ARGON2_TIME_COST`: Параметр времени Argon2
- `ARGON2_MEMORY_COST`: Параметр памяти Argon2
- `ARGON2_PARALLELISM`: Параметр параллелизма Argon2

### Переменные Frontend

- `VITE_API_URL`: URL API backend (по умолчанию: http://localhost:8000)

## Функции безопасности

### Что реализовано

✅ **Без паролей в открытом виде**: Все пароли хешируются с использованием Argon2id перед сохранением

✅ **Хеширование Argon2id**: Отраслевой стандарт хеширования паролей с настраиваемыми параметрами:
- Время: 3 (настраивается через `ARGON2_TIME_COST`)
- Память: 65536 KB (настраивается через `ARGON2_MEMORY_COST`)
- Параллелизм: 4 (настраивается через `ARGON2_PARALLELISM`)

✅ **Ограничение уникальности логина**: База данных обеспечивает уникальность значений логина

✅ **Без логирования паролей**: Пароли никогда не логируются, только имена пользователей логируются для успешных регистраций

✅ **Валидация входных данных**: И frontend, и backend валидируют входные данные согласно правилам безопасности

✅ **Защита CORS**: CORS middleware настроен для разрешения только определенных источников

### Требования к паролю

- Минимум 8 символов
- Хотя бы одна заглавная буква (A-Z)
- Хотя бы одна строчная буква (a-z)
- Хотя бы одна цифра (0-9)
- Хотя бы один специальный символ (!@#$%^&*(),.?":{}|<>)

## Схема базы данных

### Таблица Users

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(32) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

- `id`: Автоинкрементируемый первичный ключ
- `login`: Уникальное имя пользователя (3-32 символа)
- `password_hash`: Хешированный пароль Argon2id
- `created_at`: Временная метка создания аккаунта

## Разработка

### Разработка Backend

Backend использует:
- **FastAPI**: Современный Python веб-фреймворк
- **SQLAlchemy**: Асинхронный ORM для операций с базой данных
- **Pydantic**: Валидация данных и управление настройками
- **Argon2**: Библиотека хеширования паролей

### Разработка Frontend

Frontend использует:
- **React 18**: UI библиотека
- **TypeScript**: Типобезопасный JavaScript
- **Vite**: Быстрый инструмент сборки и dev сервер
- **Axios**: HTTP клиент для API вызовов

### Качество кода

- Типобезопасный код (TypeScript + Pydantic)
- Python код, соответствующий PEP 8
- Структурированное логирование (уровни INFO/ERROR)
- Комплексная обработка ошибок
- Документация OpenAPI (доступна на `/docs`)

## Логирование

Приложение использует модуль `logging` Python со структурированным выводом:

- **INFO**: Успешные операции (например, "User registered successfully")
- **ERROR**: Неудачные операции (например, "Registration failed: duplicate login")

Пароли **никогда** не логируются, только имена пользователей логируются для целей аудита.

## Документация API

FastAPI автоматически генерирует интерактивную документацию API:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Решение проблем

### Порт уже используется

Если порты 8000, 5173 или 5432 уже используются:

1. Остановите конфликтующий сервис, или
2. Измените порты в `docker-compose.yml`

### Проблемы с подключением к базе данных

Если backend не может подключиться к базе данных:

1. Убедитесь, что контейнер базы данных здоров: `docker compose ps`
2. Проверьте логи базы данных: `docker compose logs db`
3. Проверьте, что `DATABASE_URL` в `.env` соответствует настройкам docker-compose

### Frontend не может подключиться к Backend

1. Проверьте, что `VITE_API_URL` в `.env` правильный
2. Проверьте настройки CORS в `backend/main.py`
3. Убедитесь, что оба контейнера находятся в одной Docker сети

## Git Contribution

Этот проект следует чистой архитектуре с разделением ответственности:

- **Frontend** (`frontend/`): React приложение с TypeScript
- **Backend** (`backend/`): FastAPI приложение с Python
- **База данных**: Схема PostgreSQL и миграции
- **Инфраструктура**: Конфигурация Docker Compose

Каждый компонент независимо тестируем и развертываем.

## Лицензия

Это MVP проект для демонстрационных целей.

## Поддержка

По вопросам или проблемам, пожалуйста, проверьте:
1. Документацию API на http://localhost:8000/docs
2. Логи приложения: `docker compose logs`
3. Статус контейнеров: `docker compose ps`
