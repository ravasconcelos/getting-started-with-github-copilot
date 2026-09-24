from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_rejects_duplicate_email_case_insensitive():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email.upper()}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up"


def test_unregister_participant_removes_email():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email.lower()} from {activity_name}"

    activity_response = client.get("/activities")
    participants = activity_response.json()[activity_name]["participants"]
    assert email.lower() not in [participant.lower() for participant in participants]
