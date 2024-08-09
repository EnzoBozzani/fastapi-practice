from fastapi import FastAPI

from routers import windows


app = FastAPI()


app.include_router(windows.router)
