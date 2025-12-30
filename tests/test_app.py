import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Test the home route returns 200 and correct JSON."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = response.get_json()
    assert "message" in data
    assert data["status"] == "running"


def test_health_route(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["status"] == "healthy"


def test_info_route(client):
    """Test the info API endpoint."""
    response = client.get('/api/info')
    assert response.status_code == 200
    
    data = response.get_json()
    assert "app_name" in data
    assert "description" in data


def test_404_route(client):
    """Test that non-existent routes return 404."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
