from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
import asyncpg
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

# Database connection parameters
DB_USER = os.getenv("DBUSER")
DB_PASS = os.getenv("DBPASSWORD")
DB_HOST = os.getenv("DBHOST", "localhost")
DB_PORT = os.getenv("DBPORT", "5432")
DB_NAME = os.getenv("DATABASE")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     pool = await asyncpg.create_pool(DATABASE_URL)
#     yield pool
#     pool.close()
#     await pool.wait_closed()

# async def get_database():
#     pool = await asyncpg.create_pool(DATABASE_URL)
#     yield pool
#     pool.close()
#     await pool.wait_closed()

async def get_db_connection(database: asyncpg.pool.Pool):
    async with database.acquire() as connection:
        yield connection
        
@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.connect(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()



