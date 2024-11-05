# main.py

from fastapi import FastAPI
from api.main import app as api_app
import uvicorn

app = FastAPI()

# 添加带前缀的子应用
app.mount("/api/v1", api_app)

if __name__ == "__main__":
    print("Starting AI RolePlay Service...")
    print("Documentation available at: http://localhost:8000/docs")
    print("Alternative documentation at: http://localhost:8000/redoc")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )