"""Tests for registration endpoint."""
import pytest
from httpx import AsyncClient
from main import app
from database import get_db, engine, Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config import settings
import asyncio


# Create test database engine
test_engine = create_async_engine(
    settings.database_url.replace("/app", "/test_app"),
    echo=False
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def override_get_db():
    """Override database dependency for testing."""
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(scope="function")
async def setup_test_db():
    """Set up test database before each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture
async def client(setup_test_db):
    """Create test client with overridden database dependency."""
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

