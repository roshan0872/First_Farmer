def test_crop_listing_and_filters(client):
    res = client.get("/crops")
    assert res.status_code == 200
    assert b"Rice (Paddy)" in res.data

    # Search filter
    res_search = client.get("/crops?q=Rice")
    assert res_search.status_code == 200
    assert b"Rice (Paddy)" in res_search.data


def test_crop_detail_page(client):
    res = client.get("/crops/rice-paddy")
    assert res.status_code == 200
    assert b"Rice (Paddy)" in res.data
    assert b"Cultivation Guide" in res.data


def test_recommendation_matching(client):
    res = client.post("/api/recommendations", json={
        "soil_type": "Loamy",
        "season": "Kharif",
        "water_availability": "High",
        "region": "Tamil Nadu (Cauvery Delta)",
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_results"] >= 1
    assert "Preliminary educational suggestion" in data["disclaimer"]
    
    top = data["ranked_crops"][0]
    assert top["score"] >= 75
    assert top["match_category"] == "Strong match"


def test_recommendation_no_match(client):
    # Rice requires High water, so Low water excludes it
    res = client.post("/api/recommendations", json={
        "soil_type": "Loamy",
        "season": "Kharif",
        "water_availability": "Low",
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_results"] == 0


def test_bookmark_create_and_remove(student_client):
    # Add bookmark
    res_add = student_client.post("/api/bookmarks/1")
    assert res_add.status_code in [200, 201]
    assert res_add.get_json()["bookmarked"] is True

    # List bookmarks
    res_list = student_client.get("/api/bookmarks")
    assert res_list.status_code == 200
    assert len(res_list.get_json()) == 1

    # Remove bookmark
    res_del = student_client.delete("/api/bookmarks/1")
    assert res_del.status_code == 200
    assert res_del.get_json()["bookmarked"] is False

