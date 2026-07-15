import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(app_module.initial_activities)
    yield
    app_module.activities = copy.deepcopy(app_module.initial_activities)


def test_unregister_participant_removes_email_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_participant_returns_error_when_not_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert
    assert unregister_response.status_code == 400
