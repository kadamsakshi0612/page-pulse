from app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_invalid_url():
    client = app.test_client()
    response = client.post("/", data={"url":"abcd"})
    assert response.status_code == 200

def test_empty_url():
    client = app.test_client()
    response = client.post("/", data={"url":""})
    assert response.status_code == 200