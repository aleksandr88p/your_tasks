from fastapi import FastAPI
from app.routers import tasks, timelogs, stats
from app.core.database import init_db

app = FastAPI(title="YourTasks API")

app.include_router(tasks.router)
app.include_router(timelogs.router)
app.include_router(stats.router)


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}
