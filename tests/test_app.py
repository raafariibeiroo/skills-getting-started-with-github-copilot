import os
import sys

# Ensure the src folder is importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity check for one known activity
    assert 'Chess Club' in data


def test_signup_and_unregister():
    activity = 'Chess Club'
    email = 'test.user@example.com'

    # Ensure email is not present initially (clean up if needed)
    resp = client.get('/activities')
    assert resp.status_code == 200
    participants = resp.json()[activity]['participants']
    if email in participants:
        client.post(f"/activities/{activity}/unregister", params={'email': email})

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={'email': email})
    assert resp.status_code == 200
    assert 'Signed up' in resp.json().get('message', '')

    # Verify present
    resp = client.get('/activities')
    assert email in resp.json()[activity]['participants']

    # Unregister
    resp = client.post(f"/activities/{activity}/unregister", params={'email': email})
    assert resp.status_code == 200
    assert 'Unregistered' in resp.json().get('message', '')

    # Verify removed
    resp = client.get('/activities')
    assert email not in resp.json()[activity]['participants']
