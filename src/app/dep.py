from typing import Annotated

from fastapi import FastAPI
from fastapi import Depends

app = FastAPI()


class D:
    def __init__(self, arg1, arg2):
        self.args1 = arg1
        self.args2 = arg2

    def __call__(self, *args, **kwargs):
        print('начало работы с зависимостью')
        try:
            yield {"dep_value": self.args1 + self.args2}
        except Exception as e:
            # db.rollback()
            print('обработка исключения')
        finally:
            # db.commit()
            print('обработка finally')



@app.get("/user/{user_id}")
async def get_user(user_id: str, db: Annotated[dict, Depends(D('x', 'x'))] ):
    return {"user_id": user_id}