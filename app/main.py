import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import check_db_connection
from app.routers import users, tasks, login


@asynccontextmanager
async def lifespan(application: FastAPI):
    await check_db_connection()
    yield
    print("Shutdown complete")


app = FastAPI(
    title="Async Task Manager",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(login.router)
