import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def middle_log(request: Request, call_next):
    start_time = time.time()
    try:
        response  = await call_next(request)
    finally:

        end_tme = time.time()
    return response