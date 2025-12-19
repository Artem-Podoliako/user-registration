# Руководство по быстрому старту

## Одна команда для всего

```bash
docker compose up --build
```

Вот и всё! Эта единственная команда:
1. Соберет все Docker образы
2. Запустит PostgreSQL базу данных
3. Запустит FastAPI backend (порт 8000)
4. Запустит React frontend (порт 5173)

## Точки доступа

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Документация API**: http://localhost:8000/docs

## Тестовая регистрация

### Через Frontend
1. Откройте http://localhost:5173
2. Введите логин: `testuser`
3. Введите пароль: `Password123!`
4. Нажмите Зарегистрироваться

### Через curl
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"login":"testuser","password":"Password123!"}'
```

## Запуск тестов

```bash
docker compose exec backend pytest tests/ -v
```

## Остановка всего

```bash
docker compose down
```

## Решение проблем

**Конфликты портов?** Проверьте, используются ли порты 8000, 5173 или 5432.

**Не можете подключиться?** Подождите несколько секунд, пока все сервисы запустятся, затем проверьте:
```bash
docker compose ps
docker compose logs
```
