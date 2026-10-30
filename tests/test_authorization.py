def test_protected_routes_redirect_unauthenticated(client):
    res = client.get("/learning", follow_redirects=False)
    assert res.status_code == 302
    assert "/login" in res.headers["Location"]


def test_student_gets_403_on_admin(student_client):
    # Route check
    res = student_client.get("/admin/")
    assert res.status_code == 403

    # API check
    res_api = student_client.post("/api/crops", json={"name": "Forbidden Crop"})
    assert res_api.status_code == 403


def test_admin_authorized_on_admin(admin_client):
    res = admin_client.get("/admin/")
    assert res.status_code == 200
    assert b"Administrator" in res.data
