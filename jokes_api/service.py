import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete, insert

from schema import Joke, JokeCreate, JokeRead

engine = create_async_engine("sqlite+aiosqlite:///../sqlite.db")

async def create_tables():
    from sqlmodel import SQLModel
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
# create tables from schema    
asyncio.run(create_tables())

class JokeService:
    def __init__(self):
        self.async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def create_joke(self, joke_create: JokeCreate) -> Joke:
        joke = None
        async with self.async_session() as session:
            joke = Joke(**dict(joke_create))
            session.add(joke)
            await session.commit()
            await session.refresh(joke)
        return joke
    
    async def read_joke(self, id: int) -> JokeRead:
        joke_read = None
        async with self.async_session() as session:
            stmt = select(Joke).where(Joke.id == id)
            result = await session.execute(stmt)
            joke = result.scalars().one()
            joke_read = JokeRead(**dict(joke))
        return joke_read

    async def list_jokes(self) -> list[JokeRead]:
        joke_reads = []
        async with self.async_session() as session:
            stmt = select(Joke)
            result = await session.execute(stmt)
            jokes = result.scalars()
            joke_reads = list(map(lambda x : JokeRead(**dict(x)), jokes))
        return joke_reads

    async def delete_joke(self, id: int):
        async with self.async_session() as session:
            stmt = delete(Joke).where(Joke.id == id)
            result = await session.execute(stmt)
            await session.commit()
