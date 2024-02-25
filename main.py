from fastapi import FastAPI

from routes.address import address_router
from routes.client import client_router

app = FastAPI()

app.include_router(client_router)
app.include_router(address_router)
