from fastapi import FastAPI, Depends

from routers import upload, metrics
from starlette.staticfiles import StaticFiles


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(upload.router)
app.include_router(metrics.router)
