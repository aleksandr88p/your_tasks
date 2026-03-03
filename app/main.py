from fastapi import FastAPI

app = FastAPI(title="YourTasks API")


@app.get("/")
async def root():
    return {"message": "Hello World"}
