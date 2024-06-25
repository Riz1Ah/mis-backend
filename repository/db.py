from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Request
import asyncpg
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
class Database:
    def __init__(self):
        self.user = os.getenv("DBUSER")
        self.password = os.getenv("DBPASSWORD")
        self.host = os.getenv("DBHOST", "localhost")
        self.port = os.getenv("DBPORT", "5432")
        self.database = os.getenv("DATABASE")
        self._cursor = None

        self._connection_pool = None
        self.con = None

    async def connect(self):
        if not self._connection_pool:
            try:
                self._connection_pool = await asyncpg.create_pool(
                    min_size=1,
                    max_size=10,
                    command_timeout=60,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )

            except Exception as e:
                print(e)


# # Database connection parameters
# DB_USER = os.getenv("DBUSER")
# DB_PASS = os.getenv("DBPASSWORD")
# DB_HOST = os.getenv("DBHOST", "localhost")
# DB_PORT = os.getenv("DBPORT", "5432")
# DB_NAME = os.getenv("DATABASE")

# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     pool = await asyncpg.create_pool(DATABASE_URL)
#     yield pool
#     pool.close()
#     await pool.wait_closed()


