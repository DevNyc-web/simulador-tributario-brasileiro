from app import create_app


def test_app_starts():
    client = create_app().test_client()
    assert client.get("/").status_code == 200
    assert client.get("/simulacao").status_code == 200
