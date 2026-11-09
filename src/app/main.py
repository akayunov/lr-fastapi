from enum import Enum
from typing import Annotated, Any

from fastapi import FastAPI, Query, Body, HTTPException, status, Header
from fastapi.params import Depends
from pip._internal.utils import logging
from pydantic import BaseModel, field_validator, model_validator, Field, AfterValidator
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logger = logging.getLogger(__name__)


class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float
    is_offer: bool | None = None

    @field_validator('is_offer')
    @classmethod
    def is_offer_validator(cls, v: bool):
        if v:
            raise Exception('Can"t be true')
        return v

    @model_validator(mode='after')
    def model_checks(self):
        print(self.is_offer)
        return self


async def global_dep():
    logger.debug('run global dependency')
    yield
    logger.debug('finish global dependency')


app = FastAPI(dependencies=[Depends(global_dep)])


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/my")  # should be before "/items/{item_id}"
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": "my"}


def check_b(value: str):
    if value.startswith('a'):
        raise ValueError(f'{value} is not valid')


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Annotated[str | None, Query(max_length=10)] = None,
                    x: str | None = Query(default=None, min_length=10), y: Annotated[list[int], Query()] = None,
                    a: Annotated[str, Query(alias='a-query')] = None,
                    b: Annotated[str, AfterValidator(check_b)] = None):
    return {"item_id": item_id, "q": q, "x": x, "y": y[0], "a": a, "b": b}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    item.is_offer = 'нет'
    return {"item_id": item_id, "item": item.model_dump()}


class Issue(str, Enum):
    issue = "1"
    issue11 = "11"
    issue222 = "222"


@app.get("/issues/{issue_id}")
async def read_issue(issue_id: str):
    if issue_id is Issue.issue:
        return {"issue_id": issue_id}
    else:
        return {"issue_id": "other"}


@app.get("/user/{user_id}/{folder: path}")  # конвертеры на базе starlette, можно регистрировать свои
# разница между конвертером и валидатором на базе пидантик - то в какой момент времени это просходит
# ваидаторы на роутах - проверяют есть ли подходящий роут, а пидантик валидатор - проверяет, подходит ли данные для этого роута
async def get_folder(user_id: str, folder: str):
    return {"user_id": user_id, "folder": folder}


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserCreateResponse(BaseModel):
    name: str
    email: str


@app.post("/users", response_model=UserCreateResponse)
async def create_user(user: UserCreate) -> Any:
    return {"user": user}


class UserCommentsQuery(BaseModel):
    page_number: int
    page_size: int


@app.get("/user/{user_id}/comments")
async def user_comments(user_id, q: Annotated[UserCommentsQuery, Query()]):
    return {user_id: q.model_dump()}


class User(BaseModel):
    name: str


class Item(BaseModel):
    item_id: int


class CBReturn(BaseModel):
    item: Item
    flag: int


@app.post("/complex_body")
async def complex_body(item: Item, user: User, single_flag: Annotated[int, Body()]) -> CBReturn:
    if single_flag > 10:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, )
    return CBReturn(item=item, flag=1)


@app.exception_handler(HTTPException)  # глобальный обработчик ошибок
async def http_exception_handler(request: Request, exc: HTTPException) -> PlainTextResponse:
    return PlainTextResponse('trata bububu')


def increment_comment_version(x_comment_version_number: Annotated[int, Header()]):
    # complex logic
    return x_comment_version_number + 1


@app.get("/users/{user_id}/comments/{comment_id}")
async def get_comment(user_id: int, comment_id: int,
                      x_comment_version_number: Annotated[int, Depends(increment_comment_version)]) -> dict:
    return {'comment_version_number': x_comment_version_number}
