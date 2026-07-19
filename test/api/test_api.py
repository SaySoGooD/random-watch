from fastapi.testclient import TestClient

from random_watch.bootstrap import bootstrap


def test_health_check() -> None:
    with TestClient(bootstrap()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
