from fastapi import FastAPI
from app.routers import tasks, timelogs, stats

app = FastAPI(title="YourTasks API")

app.include_router(tasks.router)
app.include_router(timelogs.router)
app.include_router(stats.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
