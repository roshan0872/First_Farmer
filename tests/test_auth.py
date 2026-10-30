import pytest
from app.models.user import User, LoginAttempt
from app.services.security import is_login_locked

def test_valid_registration(client):
    res = client.post("/api/auth/register", json={
        "full_name": "Rohan Farmer",
        "email": "rohan@example.com",
        "password": "SecurePassword123!",
        "preferred_language": "en"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["user"]["email"] == "rohan@example.com"


def test_duplicate_registration_rejected(client):
    res = client.post("/api/auth/register", json={
        "full_name": "Duplicate Student",
        "email": "student@firstfarmer.org",
        "password": "Password12345!",
    })
    assert res.status_code == 409
    assert "already registered" in res.get_json()["error"]


def test_login_success_and_generic_failure(client):
    # Success
    res = client.post("/api/auth/login", json={
        "email": "student@firstfarmer.org",
        "password": "StudentPass123!"
    })
    assert res.status_code == 200
    assert res.get_json()["success"] is True

    # Generic failure message
    res_fail = client.post("/api/auth/login", json={
        "email": "nonexistent@firstfarmer.org",
        "password": "WrongPassword!"
    })
    assert res_fail.status_code == 401
    assert "incorrect" in res_fail.get_json()["error"]


def test_login_throttling_lockout(client):
    email = "target@example.com"
    for _ in range(5):
        client.post("/api/auth/login", json={"email": email, "password": "WrongPassword!"})

    res = client.post("/api/auth/login", json={"email": email, "password": "WrongPassword!"})
    assert res.status_code == 429
    assert "Too many failed attempts" in res.get_json()["error"]

