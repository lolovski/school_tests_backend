from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.main_router import main_router
from core.init_db import start_db

app = FastAPI()
app.include_router(main_router)


@app.on_event("startup")
async def startup():
    await start_db()


origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:5174',
    'http://127.0.0.1:5174',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
