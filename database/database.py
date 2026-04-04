import logging
from typing import cast

import asyncpg

from core.config import postgresql_settings
from database.models import User
from utils.meta import SingletonMeta

logger = logging.getLogger(__name__)


class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> asyncpg.Pool:
        if not self.pool:
            try:
                self.pool = await asyncpg.create_pool(
                    dsn=postgresql_settings.raw_url,
                    min_size=5,
                    max_size=20,
                    command_timeout=60,
                )
                logger.info("PostgreSQL connection pool established.")
            except Exception as e:
                logger.critical(f"Couldn't connect to PostgreSQL: {e}")
                raise e
        return self.pool

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None
            logger.info("PostgreSQL connection pool closed.")


async def get_db_conn():
    pool = await Database().connect()

    async with pool.acquire() as conn:
        yield conn


async def init_db():
    pool = await Database().connect()

    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
            """
        )
        logger.info("Database schema initialized")


async def create_user(
    db_conn: asyncpg.Connection, username: str, hashed_password: str
) -> int | None:
    query = """
        INSERT INTO users (username, hashed_password)
        VALUES ($1, $2)
        ON CONFLICT (username) DO NOTHING
        RETURNING id
    """
    result = await db_conn.fetchval(query, username, hashed_password)
    return cast(int, result) if result else None


async def get_user_by_username(
    db_conn: asyncpg.Connection, username: str
) -> User | None:
    query = """
        SELECT username, hashed_password
        FROM users
        WHERE username = $1
    """
    record = await db_conn.fetchrow(query, username)
    if record:
        return User(**record)
