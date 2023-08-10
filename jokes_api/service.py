import asyncio
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete, insert
from jokes_api.schema import Joke, JokeCreate, JokeRead

engine = create_async_engine("sqlite+aiosqlite:///../sqlite.db")

async def create_tables():
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

    async def delete_joke(self, id: int):
        async with self.async_session() as session:
            stmt = delete(Joke).where(Joke.id == id)
            result = await session.execute(stmt)
