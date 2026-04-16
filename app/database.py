from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Annotated

from app.core.config import settings

engine = create_async_engine(settings.DB_URL_asyncpg, echo=True)


AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# Dependency для сессии
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Проверка соединения с БД
async def check_db_connection() -> None:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

        print("✅ Database connected")

    except SQLAlchemyError as error:
        print("❌ Database connection failed:", error)
        raise


str_50 = Annotated[str, 50]


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    # Читаемые логи
    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.key()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f'<{self.__class__.__name__} {", ".join(cols)}>'
