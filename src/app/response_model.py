from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserCreate(BaseModel):
    username: str
    password: str


class UserCreateReturn(BaseModel):
    username: str

@app.post("/user", response_model=UserCreateReturn)
async def get_user(user: UserCreate):
    return user  # автоматом приведеться к типу UserCreateReturn