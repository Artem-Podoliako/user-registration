# Quick Start Guide

## One Command to Rule Them All

```bash
docker compose up --build
```

That's it! This single command will:
1. Build all Docker images
2. Start PostgreSQL database
3. Start FastAPI backend (port 8000)
4. Start React frontend (port 5173)

## Access Points

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Test Registration

### Via Frontend
1. Open http://localhost:5173
2. Enter login: `testuser`
3. Enter password: `Password123!`
4. Click Register

### Via curl
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"login":"testuser","password":"Password123!"}'
```

## Run Tests

```bash
docker compose exec backend pytest tests/ -v
```

## Stop Everything

```bash
docker compose down
```

## Troubleshooting

**Port conflicts?** Check if ports 8000, 5173, or 5432 are in use.

**Can't connect?** Wait a few seconds for all services to start, then check:
```bash
docker compose ps
docker compose logs
```

