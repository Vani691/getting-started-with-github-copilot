import copy

from fastapi.testclient import TestClient

import src.app as app_module


client = TestClient(app_module.app)


def setup_function():
    app_module.activities = copy.deepcopy(app_module.initial_activities)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    assert unregister_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_participant_returns_error_when_not_registered():
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    assert unregister_response.status_code == 400
