from fastapi import FastAPI
from app.db.database import init_database

app = FastAPI()

init_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Server is up and running..."}
