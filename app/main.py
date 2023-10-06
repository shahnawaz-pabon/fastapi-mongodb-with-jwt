from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.events import register_events
from app.endpoints import user

app = FastAPI()


app.include_router(user.router, tags=['Users'], prefix='/api/users')


# Register application events
register_events(app)


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')
