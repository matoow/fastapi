from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import auth

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth.api_router)

@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.get("/path-params/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/query-params/")
async def read_item(skip: int = 0, limit: int = 10, q: str | None = None):
    return  {"skip": skip, "limit": limit, "q": q}


