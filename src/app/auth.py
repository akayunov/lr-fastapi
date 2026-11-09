from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/user")
async def user(request: Request, token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.post("/token")
async def login_for_access_token():
    return {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "token_type": "bearer", "expires_in": 3600}


from fastapi import APIRouter