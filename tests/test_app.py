from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def _reset_activity_state():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]


def test_signup_adds_participant():
    # Arrange
    _reset_activity_state()
    activity_name = "Chess Club"
    test_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {test_email} for {activity_name}"
    assert test_email in activities[activity_name]["participants"]


def test_unregister_removes_participant():
    # Arrange
    _reset_activity_state()
    activity_name = "Programming Class"
    test_email = "emma@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {test_email} from {activity_name}"
    assert test_email not in activities[activity_name]["participants"]


def test_unregister_rejects_missing_participant():
    # Arrange
    _reset_activity_state()
    activity_name = "Programming Class"
    missing_email = "ghost@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={missing_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
    assert missing_email not in activities[activity_name]["participants"]
