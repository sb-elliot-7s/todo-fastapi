from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from configs import get_settings

postgres_url = get_settings().database_url

engine = create_async_engine(postgres_url, future=True, echo=True)
LocalAsyncSession = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db() -> AsyncSession:
    async with LocalAsyncSession() as session:
        yield session
