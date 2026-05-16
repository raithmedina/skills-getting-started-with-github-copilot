from urllib.parse import quote


def test_root_redirects_to_static(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_list(client):
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_registers_participant(client):
    # Arrange
    email = "teststudent@mergington.edu"
    activity = "Programming Class"
    activity_path = quote(activity, safe="")
    email_query = quote(email, safe="")

    # Act
    response = client.post(f"/activities/{activity_path}/signup?email={email_query}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Gym Class"
    email = "duplicate@mergington.edu"
    activity_path = quote(activity, safe="")
    email_query = quote(email, safe="")

    # Act
    first_response = client.post(f"/activities/{activity_path}/signup?email={email_query}")
    second_response = client.post(f"/activities/{activity_path}/signup?email={email_query}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_delete_participant_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    activity_path = quote(activity, safe="")
    email_path = quote(email, safe="")

    # Act
    response = client.delete(f"/activities/{activity_path}/participants/{email_path}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    assert email not in client.get("/activities").json()[activity]["participants"]
