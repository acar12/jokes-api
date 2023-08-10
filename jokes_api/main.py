from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from service import JokeService
from schema import Joke, JokeCreate, JokeRead

app = FastAPI()

service = JokeService()

@app.get("/", response_class=HTMLResponse)
async def index():
    return """<a href="/docs">API docs</a>"""

@app.get("/api/jokes/")
async def get_joke() -> list[JokeRead]:
    joke_reads = await service.list_jokes()
    return joke_reads

@app.get("/api/jokes/{id}")
async def get_joke(id: int) -> JokeRead:
    joke_read = await service.read_joke(id)
    return joke_read

@app.post("/api/jokes")
async def post_joke(joke_create: JokeCreate) -> Joke:
    joke = await service.create_joke(joke_create)
    return joke

@app.delete("/api/jokes/{id}")
async def delete_joke(id: int):
    await service.delete_joke(id)

if __name__ == "__main__":
    uvicorn.run("main:app")