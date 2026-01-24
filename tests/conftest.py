import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.app.db.session import get_db
from src.app.core.config import settings
from src.main import app

# Use an in-memory SQLite DB for testing logic, or separate Postgres DB
# For MVP simplicity, we will mock the DB dependency or run against the dev DB (careful!)
# Ideally, use a test container or separate DB.
# We'll use the existing Dev DB but rollback transactions.


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture that yields an async session.
    Transaction is rolled back after test.
    """
    # Create engine specifically for testing to avoid loop sharing issues

    test_engine = create_async_engine(
        str(settings.DATABASE_URI),
        echo=False,
    )

    connection = await test_engine.connect()
    transaction = await connection.begin()

    # Bind session to this connection
    session_factory = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_factory() as session:
        yield session

    await transaction.rollback()
    await connection.close()
    await test_engine.dispose()


@pytest_asyncio.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture for async HTTP client.
    Overrides get_db dependency to use the test session.
    """

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()

