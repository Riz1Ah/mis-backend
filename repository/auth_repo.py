import asyncpg
from fastapi import Depends, HTTPException

from models.user_model import User
from repository.db import get_db_connection

# User Database (for demonstration purposes)

users = {}

# In-memory session storage (for demonstration purposes)

sessions = {}
    
# @app.post("/users/")
async def create_user(user: User, connection: asyncpg.connection.Connection):
    query = "INSERT INTO users (username, password) VALUES ($1, $2) RETURNING 1"
    try:
        user_id = await connection.execute(query=query)
        return { id: user_id,"username": user.username, "password": user.password}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))