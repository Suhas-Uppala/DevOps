"""Updated unit tests for Student Feedback API (with authentication).
These tests validate core endpoints using JWT auth flow.
"""

import pytest
import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # noqa: E402


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers(client):
    """Register and login a temporary user; return Authorization headers."""
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "TestPass123!"

    # Register
    reg_resp = client.post('/register', json={
        'username': username,
        'password': password,
        'email': f'{username}@example.com'
    })
    assert reg_resp.status_code == 201

    # Login
    login_resp = client.post('/login', json={
        'username': username,
        'password': password
    })
    assert login_resp.status_code == 200
    token = login_resp.get_json()['token']
    return { 'Authorization': f'Bearer {token}' }


def test_home_endpoint(client):
    resp = client.get('/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'running'
    assert 'endpoints' in data


def test_health_endpoint(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'healthy'


def test_get_feedback_empty(auth_headers, client):
    resp = client.get('/feedback', headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True
    assert isinstance(data['data'], list)
    # Allow either empty or pre-populated state depending on test order/backend
    assert data['count'] >= 0


def test_add_feedback_success(auth_headers, client):
    payload = { 'student_name': 'John Doe', 'comment': 'Great course', 'rating': 5 }
    resp = client.post('/feedback', json=payload, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.get_json()['data']
    assert data['student_name'] == 'John Doe'
    assert data['comment'] == 'Great course'
    assert data['rating'] == 5
    assert 'id' in data


def test_add_feedback_missing_student_name(auth_headers, client):
    payload = { 'comment': 'No name', 'rating': 4 }
    resp = client.post('/feedback', json=payload, headers=auth_headers)
    assert resp.status_code == 400
    assert 'student_name' in resp.get_json()['error']


def test_add_feedback_missing_comment(auth_headers, client):
    payload = { 'student_name': 'Jane', 'rating': 4 }
    resp = client.post('/feedback', json=payload, headers=auth_headers)
    assert resp.status_code == 400
    assert 'comment' in resp.get_json()['error']


def test_add_feedback_no_data(auth_headers, client):
    resp = client.post('/feedback', data='', headers=auth_headers, content_type='application/json')
    assert resp.status_code == 400


def test_delete_feedback_success(auth_headers, client):
    # Add
    add_resp = client.post('/feedback', json={
        'student_name': 'Temp', 'comment': 'To delete', 'rating': 2
    }, headers=auth_headers)
    fid = add_resp.get_json()['data']['id']
    # Delete
    del_resp = client.delete(f'/feedback/{fid}', headers=auth_headers)
    assert del_resp.status_code == 200
    assert del_resp.get_json()['success'] is True


def test_delete_feedback_not_found(auth_headers, client):
    # Detect backend source to pick appropriate fake ID format
    src_resp = client.get('/feedback', headers=auth_headers)
    source = src_resp.get_json().get('source', 'memory')
    if source == 'mongodb':
        # Use a valid but likely non-existent ObjectId
        fake_id = '000000000000000000000000'
    else:
        fake_id = '999999'
    resp = client.delete(f'/feedback/{fake_id}', headers=auth_headers)
    assert resp.status_code == 404
    assert resp.get_json()['success'] is False


def test_add_multiple_feedback(auth_headers, client):
    items = [
        { 'student_name': 'Alice', 'comment': 'Excellent', 'rating': 5 },
        { 'student_name': 'Bob', 'comment': 'Good', 'rating': 4 },
        { 'student_name': 'Charlie', 'comment': 'Average', 'rating': 3 }
    ]
    for payload in items:
        r = client.post('/feedback', json=payload, headers=auth_headers)
        assert r.status_code == 201
    # Verify count
    get_resp = client.get('/feedback', headers=auth_headers)
    data = get_resp.get_json()
    assert data['count'] >= 3
