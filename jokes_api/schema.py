from sqlmodel import SQLModel, Field
from datetime import datetime

class JokeBase(SQLModel):
    name: str
    joke: str

# schema 

class Joke(JokeBase, table=True):
    # field definitions for ease of use
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now, nullable=False)

class JokeCreate(JokeBase):
    pass

class JokeRead(JokeBase):
    id: int
    created_at: datetime