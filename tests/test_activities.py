"""
Tests for the GET /activities endpoint.

Uses AAA (Arrange-Act-Assert) pattern for test clarity.
"""

from fastapi.testclient import TestClient


def test_get_activities_returns_all(client: TestClient, test_activities):
    """
    Test that GET /activities returns all activities with correct structure.
    
    Arrange: Test activities are set up in fixture (3 activities)
    Act: Make GET request to /activities
    Assert: Verify all activities returned with complete details
    """
    # Arrange
    expected_activity_count = 3
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_activity_count
    
    # Verify structure of activities
    assert "Test Club" in activities
    assert activities["Test Club"]["description"] == "A test club"
    assert activities["Test Club"]["schedule"] == "Mondays, 4:00 PM - 5:00 PM"
    assert activities["Test Club"]["max_participants"] == 10
    assert activities["Test Club"]["participants"] == ["alice@test.edu", "bob@test.edu"]


def test_get_activities_includes_participants(client: TestClient, test_activities):
    """
    Test that GET /activities includes current participant lists.
    
    Arrange: Test activities with known participants
    Act: Get activities from API
    Assert: Verify participants are correctly returned
    """
    # Arrange
    # (test_activities has specific participants)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    activities = response.json()
    
    # Test Club has 2 participants
    assert len(activities["Test Club"]["participants"]) == 2
    
    # Test Sports has 1 participant
    assert len(activities["Test Sports"]["participants"]) == 1
    
    # Test Art has 0 participants
    assert len(activities["Test Art"]["participants"]) == 0


def test_get_activities_response_format(client: TestClient, test_activities):
    """
    Test that GET /activities response has correct JSON structure.
    
    Arrange: Client is ready
    Act: Make GET request to /activities
    Assert: Verify response is valid dict with required fields
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    # Verify each activity has required fields
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Missing field '{field}' in activity '{activity_name}'"
        
        # Verify participants is a list
        assert isinstance(activity_data["participants"], list)
        
        # Verify max_participants is a number
        assert isinstance(activity_data["max_participants"], int)
