from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from service import JokeService, \
    Joke, JokeCreate, JokeRead # schema

app = FastAPI()

service = JokeService()

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index():
    return "<a href=\"/docs\">API docs</a>"

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
    import uvicorn
    uvicorn.run("main:app")