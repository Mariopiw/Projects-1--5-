from tests.conftest import auth_header


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_reconciliation_flow(client):
    headers = auth_header(client)
    assert client.post("/orders", json={"order_id": "ORD-1001", "sku": "ABC", "expected_qty": 10}, headers=headers).status_code == 201
    assert client.post("/warehouse-records", json={"order_id": "ORD-1001", "sku": "ABC", "actual_qty": 7}, headers=headers).status_code == 201
    result = client.post("/reconciliation/run", headers=headers)
    assert result.status_code == 200
    assert result.json()["exceptions_created"] == 1
    listed = client.get("/exceptions", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["difference"] == -3


def test_duplicate_order_returns_409(client):
    headers = auth_header(client)
    payload = {"order_id": "ORD-1", "sku": "A", "expected_qty": 1}
    assert client.post("/orders", json=payload, headers=headers).status_code == 201
    assert client.post("/orders", json=payload, headers=headers).status_code == 409


def test_viewer_cannot_create_order(client):
    headers = auth_header(client, "viewer", "viewer123")
    response = client.post("/orders", json={"order_id": "ORD-2", "sku": "A", "expected_qty": 1}, headers=headers)
    assert response.status_code == 403
