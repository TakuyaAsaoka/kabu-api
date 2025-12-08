from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ルートパスは200レスポンスを返す():
  response = client.get("/")

  assert response.status_code == 200

  data = response.json()
  assert "message" in data
  assert data["message"] == "Kabu API is running"

def test_appのメタ情報がセットされている():
  assert app.title == "Kabu API"
  assert app.description == "日本株の指標計算API"
  assert app.version == "1.0.0"
