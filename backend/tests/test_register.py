"""Tests for registration endpoint."""
import pytest
import pytest_asyncio
from httpx import AsyncClient
from main import app
from database import get_db, engine, Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.engine.url import make_url
from config import settings
import asyncio
import asyncpg


# Get test database URL
test_db_url = settings.database_url.replace("/app", "/test_app")
# Get admin database URL (connect to default postgres database to create test database)
admin_db_url = settings.database_url.replace("/app", "/postgres")


async def ensure_test_database():
    """Create test database if it doesn't exist."""
    # Parse connection URL - remove asyncpg driver prefix
    db_url_clean = admin_db_url.replace("postgresql+asyncpg://", "postgresql://")
    url = make_url(db_url_clean)
    
    # Extract connection parameters
    username = url.username or "user"
    password = url.password or "pass"
    host = url.host or "db"
    port = url.port or 5432
    
    # Connect to postgres database to create test database
    conn = await asyncpg.connect(
        user=username,
        password=password,
        host=host,
        port=port,
        database="postgres"  # Always connect to default postgres database
    )
    try:
        # Check if database exists
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", "test_app"
        )
        
        if not exists:
            # Create database (autocommit mode)
            await conn.execute("CREATE DATABASE test_app")
    finally:
        await conn.close()


# Flag to ensure database is created only once
_test_db_created = False

# We'll create engine per test to avoid event loop conflicts
def get_test_engine():
    """Create a new test engine for each test."""
    return create_async_engine(
        test_db_url,
        echo=False,
        pool_pre_ping=False,
    )

def get_test_session_local(engine):
    """Create session factory for given engine."""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


def override_get_db_factory(test_engine):
    """Create override_get_db function for given engine."""
    TestSessionLocal = get_test_session_local(test_engine)
    
    async def override_get_db():
        """Override database dependency for testing."""
        async with TestSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    
    return override_get_db


@pytest_asyncio.fixture(scope="function")
async def test_engine_fixture():
    """Create a new engine for each test to avoid event loop conflicts."""
    global _test_db_created
    
    # Create test database if it doesn't exist (only once)
    if not _test_db_created:
        await ensure_test_database()
        _test_db_created = True
    
    # Create new engine for this test
    engine = get_test_engine()
    
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: Base.metadata.create_all(bind=sync_conn, checkfirst=True)
        )
    
    # Clear all data before test
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM users"))
    
    yield engine
    
    # Clear all data after test
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM users"))
    
    # Dispose engine to clean up connections
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def setup_test_db(test_engine_fixture):
    """Set up test database before each test."""
    yield test_engine_fixture


@pytest_asyncio.fixture
async def client(setup_test_db):
    """Create test client with overridden database dependency."""
    test_engine = setup_test_db
    override_get_db = override_get_db_factory(test_engine)
    
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """Test successful user registration."""
    response = await client.post(
        "/api/register",
        json={
            "login": "testuser",
            "password": "Password123!"
        }
    )
    assert response.status_code == 201
    assert response.json() == {"message": "user created"}


@pytest.mark.asyncio
async def test_register_duplicate_login(client: AsyncClient):
    """Test registration with duplicate login returns 409."""
    # First registration
    await client.post(
        "/api/register",
        json={
            "login": "duplicateuser",
            "password": "Password123!"
        }
    )
    
    # Second registration with same login
    response = await client.post(
        "/api/register",
        json={
            "login": "duplicateuser",
            "password": "Password456@"
        }
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_weak_password(client: AsyncClient):
    """Test registration with weak password returns 422."""
    response = await client.post(
        "/api/register",
        json={
            "login": "weakpassuser",
            "password": "weak"
        }
    )
    assert response.status_code == 422
    # Check that validation error mentions password requirements
    detail = str(response.json()["detail"]).lower()
    assert any(keyword in detail for keyword in ["password", "8", "uppercase", "lowercase", "digit", "special"])

