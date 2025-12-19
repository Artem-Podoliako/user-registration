"""Database connection and session management."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings
import logging

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.app_env == "development",
    future=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables using Alembic migrations."""
    import subprocess
    import os
    import sys
    
    try:
        # Run Alembic migrations
        # Get the directory where alembic.ini is located (backend directory)
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            cwd=backend_dir,
            capture_output=True,
            text=True,
            check=False,
            timeout=30
        )
        if result.returncode == 0:
            logger.info("Database migrations applied successfully")
        else:
            logger.warning(f"Migration warning: {result.stderr or result.stdout}")
            # Fallback to create_all if migrations fail (for development)
            logger.info("Falling back to create_all for development")
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables initialized via create_all")
    except subprocess.TimeoutExpired:
        logger.warning("Migration timeout. Using create_all fallback.")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized via create_all")
    except Exception as e:
        logger.warning(f"Could not run migrations: {e}. Using create_all fallback.")
        # Fallback to create_all if Alembic is not available
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized via create_all")
