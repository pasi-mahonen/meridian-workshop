"""Tests for the /api/tasks CRUD endpoints."""

import pytest
import main as app_module


@pytest.fixture(autouse=True)
def reset_tasks():
    """Wipe the in-memory task store before each test for isolation."""
    app_module._tasks.clear()
    app_module._task_id_counter = 100
    yield
    app_module._tasks.clear()
    app_module._task_id_counter = 100


VALID_TASK = {"title": "Test task", "priority": "High", "dueDate": "2026-12-31"}


class TestGetTasks:
    def test_returns_empty_list_initially(self, client):
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_list_after_creation(self, client):
        client.post("/api/tasks", json=VALID_TASK)
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestCreateTask:
    def test_returns_201(self, client):
        response = client.post("/api/tasks", json=VALID_TASK)
        assert response.status_code == 201

    def test_response_contains_all_fields(self, client):
        response = client.post("/api/tasks", json=VALID_TASK)
        data = response.json()
        assert data["title"] == "Test task"
        assert data["priority"] == "High"
        assert data["dueDate"] == "2026-12-31"
        assert data["status"] == "pending"
        assert isinstance(data["id"], int)

    def test_id_starts_at_100(self, client):
        response = client.post("/api/tasks", json=VALID_TASK)
        assert response.json()["id"] == 100

    def test_id_increments_on_each_creation(self, client):
        id1 = client.post("/api/tasks", json=VALID_TASK).json()["id"]
        id2 = client.post("/api/tasks", json=VALID_TASK).json()["id"]
        assert id2 == id1 + 1

    def test_multiple_priorities_accepted(self, client):
        for priority in ("High", "Medium", "Low"):
            r = client.post("/api/tasks", json={**VALID_TASK, "priority": priority})
            assert r.status_code == 201
            assert r.json()["priority"] == priority

    def test_missing_title_returns_422(self, client):
        response = client.post("/api/tasks", json={"priority": "High", "dueDate": "2026-12-31"})
        assert response.status_code == 422

    def test_missing_due_date_returns_422(self, client):
        response = client.post("/api/tasks", json={"title": "Task", "priority": "High"})
        assert response.status_code == 422

    def test_missing_priority_returns_422(self, client):
        response = client.post("/api/tasks", json={"title": "Task", "dueDate": "2026-12-31"})
        assert response.status_code == 422


class TestToggleTask:
    def test_pending_becomes_completed(self, client):
        task_id = client.post("/api/tasks", json=VALID_TASK).json()["id"]
        response = client.patch(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    def test_completed_becomes_pending(self, client):
        task_id = client.post("/api/tasks", json=VALID_TASK).json()["id"]
        client.patch(f"/api/tasks/{task_id}")
        response = client.patch(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "pending"

    def test_nonexistent_task_returns_404(self, client):
        response = client.patch("/api/tasks/9999")
        assert response.status_code == 404

    def test_toggle_does_not_change_other_fields(self, client):
        task_id = client.post("/api/tasks", json=VALID_TASK).json()["id"]
        toggled = client.patch(f"/api/tasks/{task_id}").json()
        assert toggled["title"] == VALID_TASK["title"]
        assert toggled["priority"] == VALID_TASK["priority"]
        assert toggled["dueDate"] == VALID_TASK["dueDate"]


class TestDeleteTask:
    def test_returns_204(self, client):
        task_id = client.post("/api/tasks", json=VALID_TASK).json()["id"]
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204

    def test_deleted_task_not_in_list(self, client):
        task_id = client.post("/api/tasks", json=VALID_TASK).json()["id"]
        client.delete(f"/api/tasks/{task_id}")
        tasks = client.get("/api/tasks").json()
        assert not any(t["id"] == task_id for t in tasks)

    def test_nonexistent_task_returns_404(self, client):
        response = client.delete("/api/tasks/9999")
        assert response.status_code == 404

    def test_delete_only_removes_target(self, client):
        id1 = client.post("/api/tasks", json=VALID_TASK).json()["id"]
        id2 = client.post("/api/tasks", json={**VALID_TASK, "title": "Other"}).json()["id"]
        client.delete(f"/api/tasks/{id1}")
        tasks = client.get("/api/tasks").json()
        ids = [t["id"] for t in tasks]
        assert id1 not in ids
        assert id2 in ids
