from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

VALID_ORDER = {
    "customer": "maria",
    "items": [{"sku": "COFFEE-500G", "qty": 2}],
    "zip": "01001-000",
}


def test_create_order_returns_202_with_id() -> None:
    response = client.post("/orders", json=VALID_ORDER)

    assert response.status_code == 202
    body = response.json()
    assert body["status"] == "RECEIVED"
    assert len(body["id"]) == 36


def test_order_without_items_is_rejected() -> None:
    response = client.post("/orders", json={**VALID_ORDER, "items": []})

    assert response.status_code == 422


def test_order_with_zero_quantity_is_rejected() -> None:
    response = client.post("/orders", json={**VALID_ORDER, "items": [{"sku": "X", "qty": 0}]})

    assert response.status_code == 422


def test_healthz() -> None:
    assert client.get("/healthz").json() == {"status": "ok"}
