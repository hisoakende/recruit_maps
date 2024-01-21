from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from src import config

engine: AsyncEngine = None  # type: ignore
sessionmaker: async_sessionmaker = None  # type: ignore


def start_up_db() -> None:
    global engine, sessionmaker
    engine = create_async_engine(config.DB_URL)
    sessionmaker = async_sessionmaker(engine)


async def shut_down_db() -> None:
    await engine.dispose()
