"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Uses AAA (Arrange-Act-Assert) pattern for test clarity.
Includes tests for success cases, error handling, and business logic validation.
"""

from fastapi.testclient import TestClient


def test_signup_success(client: TestClient, test_activities):
    """
    Test successful signup for an activity.
    
    Arrange: Empty activity (Test Art has no participants)
    Act: Sign up a new student
    Assert: Verify student added to participants list and success message returned
    """
    # Arrange
    activity_name = "Test Art"
    student_email = "dave@test.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {student_email} for {activity_name}"
    
    # Verify student is in participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert student_email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client: TestClient, test_activities):
    """
    Test signup fails when activity doesn't exist.
    
    Arrange: Non-existent activity name
    Act: Attempt to sign up for non-existent activity
    Assert: Verify 404 error with appropriate message
    """
    # Arrange
    activity_name = "NonExistent Club"
    student_email = "eve@test.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_student(client: TestClient, test_activities):
    """
    Test that duplicate signup is prevented (student already registered).
    
    Arrange: Student already in Test Club participants
    Act: Attempt to sign up same student again
    Assert: Verify 400 error and participant list unchanged
    """
    # Arrange
    activity_name = "Test Club"
    student_email = "alice@test.edu"  # Already in Test Club
    original_participant_count = len(test_activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    
    # Verify participant count unchanged
    assert len(test_activities[activity_name]["participants"]) == original_participant_count


def test_signup_adds_participant(client: TestClient, test_activities):
    """
    Test that signup correctly adds participant to the list.
    
    Arrange: Test Club has 2 participants initially
    Act: Sign up a new student
    Assert: Verify participants count increases to 3
    """
    # Arrange
    activity_name = "Test Club"
    student_email = "frank@test.edu"
    initial_count = len(test_activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert len(test_activities[activity_name]["participants"]) == initial_count + 1
    assert student_email in test_activities[activity_name]["participants"]


def test_signup_multiple_activities(client: TestClient, test_activities):
    """
    Test that a student can sign up for multiple different activities.
    
    Arrange: Student not registered for Test Sports
    Act: Sign up for Test Sports
    Assert: Verify signup succeeds (different from Test Club where same student exists)
    """
    # Arrange
    activity_name = "Test Sports"
    student_email = "alice@test.edu"  # Already in Test Club, but NOT in Test Sports
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert student_email in test_activities[activity_name]["participants"]


def test_signup_multiple_students_same_activity(client: TestClient, test_activities):
    """
    Test that multiple different students can sign up for the same activity.
    
    Arrange: Test Art is empty
    Act: Sign up first student, then second student
    Assert: Both students are in participants list
    """
    # Arrange
    activity_name = "Test Art"
    student1 = "george@test.edu"
    student2 = "hannah@test.edu"
    
    # Act - First signup
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student1}
    )
    
    # Act - Second signup
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student2}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert student1 in test_activities[activity_name]["participants"]
    assert student2 in test_activities[activity_name]["participants"]
    assert len(test_activities[activity_name]["participants"]) == 2


def test_signup_url_encoding(client: TestClient, test_activities):
    """
    Test that activity names with spaces are properly handled.
    
    Arrange: Activity name with space "Test Club"
    Act: Sign up using properly encoded URL
    Assert: Verify signup works with encoded activity name
    """
    # Arrange
    activity_name = "Test Club"
    student_email = "iris@test.edu"
    
    # Act - Activity name will be URL encoded by the client
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert student_email in test_activities[activity_name]["participants"]


def test_signup_response_message_format(client: TestClient, test_activities):
    """
    Test that signup response message has correct format.
    
    Arrange: Ready to sign up
    Act: Perform signup
    Assert: Verify message format is "<email> for <activity>"
    """
    # Arrange
    activity_name = "Test Art"
    student_email = "jack@test.edu"
    expected_message = f"Signed up {student_email} for {activity_name}"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == expected_message
