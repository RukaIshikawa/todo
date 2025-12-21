# uvicorn backend.api.main:app --reload --reload --workers 1 --host 0.0.0.0 --port 8000
# http://localhost:8000/docs
from fastapi import FastAPI, Request, status, Query, Header, Response, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .routers import task, done, user

app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)
app.include_router(user.router)


@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.get("/hello")
async def hello():
    return {"message": "hello world!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/greet")
async def greet_user(name: str ="ゲスト"):
    return {"message": f"こんにちは、{name}さん！"}

@app.get("/search/")
async def search_items(keyword: str = Query(..., min_length=2, max_length=20, description="検索ワード")):
    return {"result": f"'{keyword}' で検索しました"}

@app.get("/users/{user_id}")
async def get_user_data(user_id: int, detail: bool = False):
    return {"user_id": user_id, "detail": detail}

class User(BaseModel):
    username: str
    email: str
    age: int

@app.post("/users/")
async def create_user(user: User):
    return {"message": f"{user.username}さんを登録しました", "email": user.email}

@app.get("/header-check")
async def check_header(user_agent: str = Header(default=None)):
    return {"user_agent": user_agent}

@app.get("/custom-header")
async def custom_header(response: Response):
    response.headers["X-Custom-Header"] = "これはカスタムヘッダーです"
    return {"message": "ヘッダーを設定しました"}

@app.get("/secure-data")
async def secure_data(token: str = Header(...)):
    if token != "mysecrettoken":
        raise HTTPException(status_code=403, detail="認証失敗")
    return {"data": "これは保護された情報です"}
