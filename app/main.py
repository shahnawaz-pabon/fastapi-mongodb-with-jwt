from fastapi import FastAPI
from app.core.events import register_events

app = FastAPI()

# Register application events
register_events(app)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Server is up and running..."}
