from unittest.mock import patch
import requests
from app.services.chatbot import ChatbotService
from app.services.weather import fetch_weather_for_location

def test_chatbot_known_and_unknown_questions(client):
    # Known FAQ query
    res_faq = client.post("/api/chat", json={"message": "How do I do a soil test?"})
    assert res_faq.status_code == 200
    data_faq = res_faq.get_json()
    assert "soil test" in data_faq["answer"].lower() or "kvk" in data_faq["answer"].lower()

    # Unknown query -> honest fallback
    res_unk = client.post("/api/chat", json={"message": "What is the quantum speed of a Martian hovercraft?"})
    assert res_unk.status_code == 200
    data_unk = res_unk.get_json()
    assert "could not find a verified answer" in data_unk["answer"].lower()


def test_weather_fallback_without_key(client):
    res = client.get("/api/weather?location=Coimbatore")
    assert res.status_code == 200
    data = res.get_json()
    assert data["is_live"] is False
    assert "Sample data — not live weather." in data["notice"]


def test_weather_with_mocked_api(app):
    with app.app_context():
        app.config["WEATHER_API_KEY"] = "mock-valid-key"

        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "name": "Coimbatore",
                "sys": {"country": "IN"},
                "main": {"temp": 31.5, "humidity": 65},
                "wind": {"speed": 4.5},
                "weather": [{"description": "clear sky"}]
            }

            data = fetch_weather_for_location("Coimbatore")
            assert data["is_live"] is True
            assert data["temperature_c"] == 31.5
            assert "Coimbatore, IN" in data["location"]


def test_weather_timeout_handling(app):
    with app.app_context():
        app.config["WEATHER_API_KEY"] = "mock-valid-key"

        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            data = fetch_weather_for_location("Coimbatore")
            assert "error" in data
            assert "timed out" in data["error"]


def test_language_switching(client):
    res = client.get("/set-language/ta", follow_redirects=False)
    assert res.status_code == 302
    assert "pref_lang=ta" in str(res.headers)


def test_healthz_endpoint(client):
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.get_json()["status"] == "healthy"
