from fastapi import FastAPI, Response
from fastapi.routing import APIRouter

# Роутер для пользователей
router1 = APIRouter(prefix="/users", tags=["users"])

@router1.get("/")
async def user_get():
    return {}

@router1.post("/{user_id}")
async def user_create(user_id: str):  # Добавили user_id в аргументы
    return Response(status_code=201)  # Возвращаем объект ответа


# Роутер для комментариев, привязанных к пользователю
router2 = APIRouter(prefix="/users/{user_id}/comments", tags=["comments"])

@router2.get("/")
async def comment_get(user_id: str):  # Добавили user_id из префикса
    return {}

@router2.post("/{comment_id}")
async def comment_create(user_id: str, comment_id: str):  # Добавили оба параметра
    return Response(status_code=201)


app = FastAPI()

app.include_router(router1)
app.include_router(router2)