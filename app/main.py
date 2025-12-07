from fastapi import FastAPI
from .routers import rsi

app = FastAPI(
  title="Kabu API",
  description="日本株の指標計算API",
  version="1.0.0"
)

app.include_router(rsi.router)

@app.get("/")
def root():
  return {"message": "Kabu API is running"}