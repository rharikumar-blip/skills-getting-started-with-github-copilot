from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    test_email = "newstudent@mergington.edu"

    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    signup_response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert signup_response.status_code == 200
    assert test_email in activities[activity_name]["participants"]

    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unregister_response.status_code == 200
    assert test_email not in activities[activity_name]["participants"]


def test_unregister_rejects_missing_participant():
    activity_name = "Programming Class"
    missing_email = "ghost@mergington.edu"

    activities[activity_name]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]

    response = client.delete(f"/activities/{activity_name}/unregister?email={missing_email}")
    assert response.status_code == 404
