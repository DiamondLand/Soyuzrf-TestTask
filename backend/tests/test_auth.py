def test_register_user(client):
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user(client):
    client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    response = client.post("/auth/login", data={"username": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
