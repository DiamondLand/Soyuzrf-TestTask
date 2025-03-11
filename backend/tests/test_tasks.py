def test_create_task(client):
    token = client.post("/auth/register", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/tasks/", 
        json={"title": "Test Task", "deadline": "2030-12-31T23:59:59", "priority": "medium"}, 
        headers=headers
    )
    
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_get_tasks(client):
    token = client.post("/auth/register", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/tasks/", json={"title": "Test Task", "deadline": "2030-12-31T23:59:59", "priority": "medium"}, headers=headers)
    response = client.get("/tasks/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_task(client):
    token = client.post("/auth/register", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    task = client.post("/tasks/", json={"title": "Old Title", "deadline": "2030-12-31T23:59:59", "priority": "medium"}, headers=headers).json()
    task_id = task["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Title"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_task(client):
    token = client.post("/auth/register", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    task = client.post("/tasks/", json={"title": "Task to Delete", "deadline": "2030-12-31T23:59:59", "priority": "medium"}, headers=headers).json()
    task_id = task["id"]

    response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200

    response = client.get("/tasks/", headers=headers)
    assert all(task["id"] != task_id for task in response.json())
