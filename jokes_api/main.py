from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from service import JokeService, \
    Joke, JokeCreate, JokeRead # schema


app = FastAPI()
origins = ["http://127.0.0.1", "http://127.0.0.1:8080", "http://127.0.0.1:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

service = JokeService()

@app.get("/api/jokes/")
async def get_joke() -> list[JokeRead]:
    joke_reads = await service.list_jokes()
    return joke_reads

@app.get("/api/jokes/{id}")
async def get_joke(id: int) -> JokeRead:
    joke_read = await service.read_joke(id)
    return joke_read

@app.post("/api/jokes/")
async def post_joke(joke_create: JokeCreate) -> Joke:
    joke = await service.create_joke(joke_create)
    return joke

@app.delete("/api/jokes/{id}")
async def delete_joke(id: int):
    await service.delete_joke(id)

if __name__ == "__main__":
    # run uvicorn
    import uvicorn
    uvicorn.run("main:app")