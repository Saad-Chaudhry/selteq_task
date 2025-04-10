import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from core.models import Task
from .factories import UserFactory, TaskFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def another_user():
    return UserFactory()


@pytest.fixture
def auth_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return client


@pytest.fixture
def unauth_client():
    return APIClient()


@pytest.fixture
def create_tasks(user):
    return TaskFactory.create_batch(5, user=user)


@pytest.mark.django_db
def test_create_task_valid(auth_client):
    response = auth_client.post("/api/v1/task/", {"title": "Task A", "duration": 30})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_task_unauthorized(unauth_client):
    response = unauth_client.post("/api/v1/task/", {"title": "Task B", "duration": 30})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_task_missing_title(auth_client):
    response = auth_client.post("/api/v1/task/", {"duration": 30})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_task_missing_duration(auth_client):
    response = auth_client.post("/api/v1/task/", {"title": "Task C"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_task_invalid_duration(auth_client):
    response = auth_client.post("/api/v1/task/", {"title": "Task D", "duration": "abc"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_task_empty_title(auth_client):
    response = auth_client.post("/api/v1/task/", {"title": "", "duration": 20})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_task_list(auth_client, create_tasks):
    response = auth_client.get("/api/v1/task/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 4


@pytest.mark.django_db
def test_get_task_list_empty(auth_client):
    response = auth_client.get("/api/v1/task/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_get_task_list_unauthenticated(unauth_client):
    response = unauth_client.get("/api/v1/task/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_retrieve_task_valid(auth_client, create_tasks):
    task = create_tasks[0]
    response = auth_client.get(f"/api/v1/task/{task.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == task.title


@pytest.mark.django_db
def test_retrieve_task_not_found(auth_client):
    response = auth_client.get("/api/v1/task/999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_task_title(auth_client, create_tasks):
    task = create_tasks[0]
    response = auth_client.put(f"/api/v1/task/{task.id}/", {"title": "Updated Title"})
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == "Updated Title"


@pytest.mark.django_db
def test_update_task_invalid_id(auth_client):
    response = auth_client.put("/api/v1/task/999/", {"title": "Updated Title"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == "Task not found"


@pytest.mark.django_db
def test_update_task_missing_duration(auth_client, create_tasks):
    task = create_tasks[0]
    response = auth_client.put(f"/api/v1/task/{task.id}/", {"title": "Updated Title"})
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == "Updated Title"
    assert task.duration == task.duration


@pytest.mark.django_db
def test_delete_task_valid(auth_client, create_tasks):
    task = create_tasks[0]
    response = auth_client.delete(f"/api/v1/task/{task.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_task_not_found(auth_client):
    response = auth_client.delete("/api/v1/task/999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_retrieve_other_user_task(auth_client, another_user):
    task = TaskFactory(user=another_user)
    response = auth_client.get(f"/api/v1/task/{task.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_other_user_task(auth_client, another_user):
    task = TaskFactory(user=another_user)
    response = auth_client.delete(f"/api/v1/task/{task.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
