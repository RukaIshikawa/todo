from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "hello world!"}

# uvicorn backend.api.main:app --reload --reload --workers 1 --host 0.0.0.0 --port 8000
# http://localhost:8000/docs