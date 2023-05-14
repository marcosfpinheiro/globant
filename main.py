from fastapi import FastAPI, Depends

from routers import upload, metrics
from starlette import status
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse("/upload", status_code=status.HTTP_302_FOUND)

app.include_router(upload.router)
app.include_router(metrics.router)

