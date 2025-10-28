"""
Unit tests for Student Feedback API
Tests all endpoints and functionality
"""

import pytest
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test the home endpoint returns API information"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'Student Feedback' in data['message']


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_get_feedback_empty(client):
    """Test getting feedback when list is empty"""
    response = client.get('/feedback')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert isinstance(data['data'], list)


def test_add_feedback_success(client):
    """Test adding new feedback successfully"""
    feedback_data = {
        'student_name': 'John Doe',
        'comment': 'Great course! Learned a lot.',
        'rating': 5
    }
    
    response = client.post('/feedback', 
                          json=feedback_data,
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['student_name'] == 'John Doe'
    assert data['data']['comment'] == 'Great course! Learned a lot.'
    assert data['data']['rating'] == 5
    assert 'id' in data['data']


def test_add_feedback_missing_student_name(client):
    """Test adding feedback without student_name"""
    feedback_data = {
        'comment': 'Great course!',
        'rating': 5
    }
    
    response = client.post('/feedback',
                          json=feedback_data,
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'student_name' in data['error']


def test_add_feedback_missing_comment(client):
    """Test adding feedback without comment"""
    feedback_data = {
        'student_name': 'Jane Doe',
        'rating': 4
    }
    
    response = client.post('/feedback',
                          json=feedback_data,
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'comment' in data['error']


def test_add_feedback_no_data(client):
    """Test adding feedback with no data"""
    response = client.post('/feedback',
                          data='',
                          content_type='application/json')
    
    assert response.status_code == 400


def test_delete_feedback_success(client):
    """Test deleting feedback successfully"""
    # First add a feedback
    feedback_data = {
        'student_name': 'Test Student',
        'comment': 'Test comment',
        'rating': 3
    }
    
    add_response = client.post('/feedback',
                               json=feedback_data,
                               content_type='application/json')
    
    feedback_id = add_response.get_json()['data']['id']
    
    # Now delete it
    delete_response = client.delete(f'/feedback/{feedback_id}')
    assert delete_response.status_code == 200
    data = delete_response.get_json()
    assert data['success'] is True


def test_delete_feedback_not_found(client):
    """Test deleting non-existent feedback"""
    response = client.delete('/feedback/99999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False


def test_add_multiple_feedback(client):
    """Test adding multiple feedback entries"""
    feedback_list = [
        {'student_name': 'Alice', 'comment': 'Excellent!', 'rating': 5},
        {'student_name': 'Bob', 'comment': 'Good course', 'rating': 4},
        {'student_name': 'Charlie', 'comment': 'Average', 'rating': 3}
    ]
    
    for feedback in feedback_list:
        response = client.post('/feedback',
                              json=feedback,
                              content_type='application/json')
        assert response.status_code == 201
    
    # Check if all feedback is stored
    get_response = client.get('/feedback')
    data = get_response.get_json()
    assert data['count'] >= 3
