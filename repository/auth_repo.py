import asyncpg
from fastapi import Depends, HTTPException

from models.user_model import User

# User Database (for demonstration purposes)

users = {}

# In-memory session storage (for demonstration purposes)

sessions = {}
    
# @app.post("/users/")
async def create_user(user: User, connection: asyncpg.connection.Connection):
    query = "INSERT INTO users (username, password) VALUES ($1, $2) RETURNING 1"
    user_id = await connection.fetchval(query, user.username, user.password)
    return { id: user_id,"username": user.username, "password": user.password}

async def get_user(user: str, connection: asyncpg.connection.Connection):
    query = " select username from users where username = $1"
    user_id = await connection.fetchval(query, user.username)
    return { "username": user_id}

async def get_creds(user: str, connection: asyncpg.connection.Connection):
    query = " select username,password from users where username = $1"
    creds= await connection.fetchval(query, user.username)
    return creds