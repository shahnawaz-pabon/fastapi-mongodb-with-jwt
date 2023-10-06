from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.events import register_events

app = FastAPI()

# Register application events
register_events(app)


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')
