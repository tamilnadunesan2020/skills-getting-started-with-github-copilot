"""
Pytest configuration and fixtures for FastAPI tests.

Fixtures provide:
- Fresh app instance with isolated test data
- TestClient for making HTTP requests
- Sample test activities for testing
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient for the FastAPI app.
    
    Each test gets a fresh app instance with isolated data.
    """
    return TestClient(app)


@pytest.fixture
def test_activities():
    """
    Provide clean test activities data for each test.
    
    This fixture captures the activities state before test execution
    and resets it after, ensuring test isolation.
    """
    # Save original state
    original_activities = {name: details.copy() for name, details in activities.items()}
    
    # Clear and set up fresh test data
    activities.clear()
    activities.update({
        "Test Club": {
            "description": "A test club",
            "schedule": "Mondays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["alice@test.edu", "bob@test.edu"]
        },
        "Test Sports": {
            "description": "A test sports activity",
            "schedule": "Wednesdays, 3:00 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["charlie@test.edu"]
        },
        "Test Art": {
            "description": "A test art activity",
            "schedule": "Fridays, 2:00 PM - 3:30 PM",
            "max_participants": 15,
            "participants": []
        }
    })
    
    yield activities
    
    # Restore original state
    activities.clear()
    activities.update(original_activities)
