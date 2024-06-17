from contextlib import asynccontextmanager
import asyncpg
from fastapi import APIRouter, FastAPI, HTTPException,status, Depends
from fastapi import Body

from models.user_model import User
from repository import auth_repo
from repository.db import DATABASE_URL
from services import auth_service

#let's create router
router = APIRouter(
prefix='/auth',
tags = ['authentication']
)

# # Get current user endpoint - Returns the user corresponding to the session ID
# @router.get("/getusers/me")
# def read_current_user(user: dict = Depends(get_user_from_session_id)):
# return user

# Protected endpoint - Requires authentication
@router.get("/protected")
def protected_endpoint(user: dict = Depends(auth_service.get_authenticated_user_from_session_id)):
  if user is None:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
  return {"message": "This user can connect to a protected endpoint after successfully autheticated", "user": user}

@router.post("/signup")
async def sign_up(username: str = Body(...), password: str = Body(...)):
  print(username)
  user = auth_repo.users.get(username)
  if user:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="Username already exists",
    )
  new_user_id = len(auth_repo.users) + 1
  new_user = User(
    username= username,
    password= password
    # "user_id": new_user_id
  )
  # auth_repo.users[username] = new_user
  async with router.lifespan as connection:
    await auth_repo.create_user(new_user,connection)
  return {"message": "User registered successfully"}

@router.post("/check-account")
def check_account(username: str = Body(...),password: str = Body(...)):
  # print(username)
  user = auth_service.check_if_user_exists(username)
  if user:
    return {"userExists": True}
  return {"userExists":False}
# Login endpoint - Creates a new session

@router.post("/login")
def login(user: dict = Depends(auth_service.authenticate_user)):
  session_id = auth_service.create_session(user["user_id"])
  return {"message": "success", "session_id": session_id}

# Logout endpoint - Removes the session
@router.post("/logout")
def logout(session_id: int = Depends(auth_service.get_session_id)):
  if session_id not in auth_repo.sessions:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
  auth_repo.sessions.pop(session_id)
  return {"message": "Logged out successfully", "session_id": session_id}

