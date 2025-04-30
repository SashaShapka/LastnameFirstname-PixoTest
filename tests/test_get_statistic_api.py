from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_statistic():
    user = {
        "username": "stat_admin",
        "password": "strongpass",
        "role": "admin"
    }

    res_signup = client.post("/sign-up", json=user)
    assert res_signup.status_code in (200, 201)
    token = res_signup.json()["access_token"]

    # GET /get_statistic?values_on_the_top=3
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/statistic_product", headers=headers, params={"values_on_the_top": 3})

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 3
    for item in data:
        assert "product_id" in item
        assert "name" in item
        assert "times_chosen" in item
