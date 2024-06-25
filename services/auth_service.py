from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException,status, Depends,Request

import random
from typing import Annotated

from repository import auth_repo

security = HTTPBasic()

def check_if_user_exists(username: str, connection):
  user = auth_repo.get_user(username,connection)
  if user is None:
    return False
  return True

async def authenticate_user(request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
  async with request.app.state.db._connection_pool.acquire() as connection:
    user = auth_repo.get_creds(username,connection)
  if user is None or user["password"] != credentials.password:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid credentials",
      headers={"WWW-Authenticate": "Basic"},
    )
  return user

def create_session(user_id: int):
  session_id = len(auth_repo.sessions) + random.randint(0, 1000000)
  auth_repo.sessions[session_id] = user_id
  return session_id

# Custom middleware for session-based authentication
def get_authenticated_user_from_session_id(request: Request):
  session_id = request.cookies.get("session_id")
  if session_id is None or int(session_id) not in auth_repo.sessions:
    raise HTTPException(
      status_code=401,
      detail="Invalid session ID",
    )

  # Get the user from the session
  user = get_user_from_session(int(session_id))
  return user

# Use the valid session id to get the corresponding user from the users dictionary
def get_user_from_session(session_id: int):
  user = None
  for user_data in auth_repo.users.values():
    if user_data['user_id'] == auth_repo.sessions.get(session_id):
      user = user_data
      break
  return user

# Create a new dependency to get the session ID from cookies
def get_session_id(request: Request):
  session_id = request.cookies.get("session_id")
  if session_id is None or int(session_id) not in auth_repo.sessions:
    raise HTTPException(status_code=401, detail="Invalid session ID")
  return int(session_id)















