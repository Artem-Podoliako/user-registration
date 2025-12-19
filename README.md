# User Registration MVP

A complete minimum viable product (MVP) implementing a user registration system with a modern full-stack architecture.

## Architecture

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Containerization**: Docker Compose

## Project Structure

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

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (optional, for cloning)

### Running the Application

1. **Clone or navigate to the project directory**

2. **Start all services with a single command:**

```bash
docker compose up --build
```

This command will:
- Build the frontend, backend, and database containers
- Start PostgreSQL database
- Start FastAPI backend on port 8000
- Start React frontend on port 5173
- Set up networking between services

3. **Access the application:**

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc

### Stopping the Application

```bash
docker compose down
```

To also remove volumes (database data):

```bash
docker compose down -v
```

## API Endpoints

### POST /api/register

Register a new user.

**Request Body:**
```json
{
  "login": "user123",
  "password": "Password123!"
}
```

**Validation Rules:**
- `login`: 3-32 characters, only letters, numbers, dots, underscores, or hyphens
- `password`: Minimum 8 characters, must include:
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  - At least one special character

**Responses:**

- **201 Created**: Success
  ```json
  {
    "message": "user created"
  }
  ```

- **422 Unprocessable Entity**: Validation error
  ```json
  {
    "detail": "Password must contain at least one uppercase letter"
  }
  ```

- **409 Conflict**: Duplicate login
  ```json
  {
    "detail": "Login already exists"
  }
  ```

## Example Usage

### Using curl

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"login":"testuser","password":"Password123!"}'
```

### Using the Frontend

1. Open http://localhost:5173 in your browser
2. Fill in the registration form:
   - **Login**: Enter a username (3-32 chars, letters/numbers/._-)
   - **Password**: Enter a strong password (min 8 chars with uppercase, lowercase, digit, special char)
3. Click "Register"
4. On success, you'll see "user created" message
5. On error, validation messages will be displayed

## Testing

### Running Backend Tests

```bash
# Enter the backend container
docker compose exec backend bash

# Run tests
pytest tests/ -v
```

Or run tests directly:

```bash
docker compose exec backend pytest tests/ -v
```

### Test Coverage

The test suite includes:

1. **test_register_success**: Tests successful user registration
2. **test_register_duplicate_login**: Tests 409 error on duplicate login
3. **test_weak_password**: Tests 422 error on invalid password strength

## Environment Variables

The application uses environment variables defined in `.env` file. See `.env.example` for reference.

### Backend Variables

- `DATABASE_URL`: PostgreSQL connection string
- `HASH_SCHEME`: Password hashing scheme (argon2)
- `SECRET_KEY`: Secret key for application
- `APP_ENV`: Environment (development/production)
- `PORT`: Backend port (default: 8000)
- `ARGON2_TIME_COST`: Argon2 time cost parameter
- `ARGON2_MEMORY_COST`: Argon2 memory cost parameter
- `ARGON2_PARALLELISM`: Argon2 parallelism parameter

### Frontend Variables

- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

## Security Features

### What's Implemented

✅ **No Plaintext Passwords**: All passwords are hashed using Argon2id before storage

✅ **Argon2id Hashing**: Industry-standard password hashing with configurable parameters:
- Time cost: 3 (configurable via `ARGON2_TIME_COST`)
- Memory cost: 65536 KB (configurable via `ARGON2_MEMORY_COST`)
- Parallelism: 4 (configurable via `ARGON2_PARALLELISM`)

✅ **Unique Login Constraint**: Database enforces unique login values

✅ **No Password Logging**: Passwords are never logged, only login names are logged for successful registrations

✅ **Input Validation**: Both frontend and backend validate input according to security rules

✅ **CORS Protection**: CORS middleware configured to allow only specific origins

### Password Requirements

- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)
- At least one special character (!@#$%^&*(),.?":{}|<>)

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(32) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

- `id`: Auto-incrementing primary key
- `login`: Unique username (3-32 characters)
- `password_hash`: Argon2id hashed password
- `created_at`: Timestamp of account creation

## Development

### Backend Development

The backend uses:
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Async ORM for database operations
- **Pydantic**: Data validation and settings management
- **Argon2**: Password hashing library

### Frontend Development

The frontend uses:
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and dev server
- **Axios**: HTTP client for API calls

### Code Quality

- Type-safe code (TypeScript + Pydantic)
- PEP 8 compliant Python code
- Structured logging (INFO/ERROR levels)
- Comprehensive error handling
- OpenAPI documentation (available at `/docs`)

## Logging

The application uses Python's `logging` module with structured output:

- **INFO**: Successful operations (e.g., "User registered successfully")
- **ERROR**: Failed operations (e.g., "Registration failed: duplicate login")

Passwords are **never** logged, only login names are logged for audit purposes.

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Troubleshooting

### Port Already in Use

If ports 8000, 5173, or 5432 are already in use:

1. Stop the conflicting service, or
2. Modify ports in `docker-compose.yml`

### Database Connection Issues

If the backend can't connect to the database:

1. Ensure the database container is healthy: `docker compose ps`
2. Check database logs: `docker compose logs db`
3. Verify `DATABASE_URL` in `.env` matches docker-compose settings

### Frontend Can't Reach Backend

1. Verify `VITE_API_URL` in `.env` is correct
2. Check CORS settings in `backend/main.py`
3. Ensure both containers are on the same Docker network

## Git Contribution

This project follows a clean architecture with separate concerns:

- **Frontend** (`frontend/`): React application with TypeScript
- **Backend** (`backend/`): FastAPI application with Python
- **Database**: PostgreSQL schema and migrations
- **Infrastructure**: Docker Compose configuration

Each component is independently testable and deployable.

## License

This is an MVP project for demonstration purposes.

## Support

For issues or questions, please check:
1. API documentation at http://localhost:8000/docs
2. Application logs: `docker compose logs`
3. Container status: `docker compose ps`

