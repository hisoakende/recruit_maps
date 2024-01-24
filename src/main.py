from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src import config
from src.database import start_up_db, shut_down_db
from src.tags.router import router as tags_router
from src.users.router import router as users_router

app = FastAPI(title='Recruit Maps')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tags_router)
app.include_router(users_router)

app.mount('/storage', StaticFiles(directory=config.STORAGE_PATH), name='storage')


@app.on_event('startup')
def start_up() -> None:
    start_up_db()


@app.on_event('shutdown')
async def shut_down():
    await shut_down_db()
