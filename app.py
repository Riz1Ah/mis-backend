from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from repository.db import Database
from services import communication_details_service as cds
from routes import auth_routes

app = FastAPI()
origins = ["*"]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    database_instance = Database()
    await database_instance.connect()
    app.state.db = database_instance

@app.on_event("shutdown")
async def shutdown():
    await app.state.db._connection_pool.close()

app.include_router(auth_routes.router)

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
  return {"item_id": item_id, "q": q}

@app.get("/comm_details")
def get_communication_details():
  cds.save_data_to_excel()

# fastapi dev app.py

