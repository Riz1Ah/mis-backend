from contextlib import asynccontextmanager
from typing import Union

import asyncpg
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

from repository.db import DATABASE_URL
from services import communication_details_service as cds
from repository import auth_repo
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

app.include_router(auth_routes.router)
# Lifespan context for managing database connection pool
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await asyncpg.create_pool(DATABASE_URL)
    yield
    await app.state.db.close()

# Include the lifespan in the FastAPI app
app.router.lifespan = lifespan

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

