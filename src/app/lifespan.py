from typing import Annotated

from fastapi import FastAPI
from fastapi import Depends



async def lifespan(app: FastAPI):
    print('on start app')
    try:
        yield
    finally:
        print('on end application')


app = FastAPI(lifespan=lifespan)




@app.get("/user/{user_id}")
async def get_user(user_id: str, db: Annotated[dict, Depends(D('x', 'x'))] ):
    return {"user_id": user_id}