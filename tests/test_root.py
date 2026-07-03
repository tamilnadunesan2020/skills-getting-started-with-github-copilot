"""
Tests for the root endpoint (GET /).

Uses AAA (Arrange-Act-Assert) pattern for test clarity.
"""

from fastapi.testclient import TestClient


def test_root_redirects_to_index(client: TestClient, test_activities):
    """
    Test that GET / redirects to /static/index.html.
    
    Arrange: Client is ready (from fixture)
    Act: Make GET request to /
    Assert: Verify redirect status and location
    """
    # Arrange
    # (client fixture already prepared)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"


def test_root_redirects_with_follow(client: TestClient, test_activities):
    """
    Test that following the redirect from / works correctly.
    
    Arrange: Client is ready
    Act: Make GET request to / with redirect following
    Assert: Verify final response is successful
    """
    # Arrange
    # (client fixture already prepared)
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
