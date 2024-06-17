from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    # session_id: int
    # token:str