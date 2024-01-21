from src import database


async def get_db_session() -> None:
    async with database.sessionmaker() as session:
        yield session
