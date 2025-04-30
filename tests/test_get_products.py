from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_products_with_cache():
    user = {
        "username": "product_tester",
        "password": "supersecret",
        "role": "admin"
    }

    res_signup = client.post("/sign-up", json=user)
    assert res_signup.status_code == 200
    token = res_signup.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/get_products", headers=headers)

    assert res.status_code == 200
    print(res.json())