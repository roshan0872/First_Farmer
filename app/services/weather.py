import requests
from flask import current_app

def get_agricultural_weather_advisory(temp_c: float, humidity: int, condition: str, wind_speed_kmh: float) -> list[str]:
    """Generate practical educational farming guidance based on current weather conditions."""
    advisories = []

    # Rain / Humidity advisory
    if "rain" in condition.lower() or "drizzle" in condition.lower() or humidity > 80:
        advisories.append("High moisture / precipitation risk: Postpone foliar spraying of fertilizers and protectants to avoid rain wash-off.")
        advisories.append("Harvest precaution: Delay threshing and combine harvesting; avoid storing damp grains or pods to prevent fungal mold.")
        advisories.append("Field drainage: Check drains in low-lying plots to avoid waterlogging in sensitive crops like maize and tomato.")
    elif humidity < 40:
        advisories.append("Low humidity dry spell: Monitor soil moisture closely; consider evening micro-irrigation or organic mulching.")

    # Temperature advisory
    if temp_c > 35:
        advisories.append("Heat stress alert: Provide light, frequent irrigations during early morning or evening hours; avoid mid-day nitrogen fertilizer application.")
    elif temp_c < 12:
        advisories.append("Cool conditions: Favorable for winter rabi crops (wheat, barley); monitor for yellow rust symptoms under morning dew.")

    # Wind advisory
    if wind_speed_kmh > 25:
        advisories.append("High wind speed: Refrain from spray operations due to drift loss; provide bamboo prop support for heavy banana bunches.")
    else:
        advisories.append("Favorable wind conditions: Suitable for precision field spray and pollination.")

    return advisories


def fetch_weather_for_location(location: str) -> dict:
    """
    Fetch live weather if WEATHER_API_KEY is configured; otherwise return explicit sample data.
    """
    api_key = current_app.config.get("WEATHER_API_KEY")
    loc = location.strip() if location else "Coimbatore"

    # If no API key configured, return explicit sample fallback
    if not api_key:
        sample_data = {
            "is_live": False,
            "provider": "Sample Educational Provider (No API key configured)",
            "notice": "Sample data — not live weather.",
            "location": loc,
            "temperature_c": 28.5,
            "humidity_percent": 68,
            "wind_speed_kmh": 12.0,
            "condition": "Partly Cloudy",
            "forecast_summary": "Scattered clouds with mild breeze. Day highs near 30°C.",
            "advisories": get_agricultural_weather_advisory(28.5, 68, "Partly Cloudy", 12.0),
            "updated_at": "Educational Simulation",
        }
        return sample_data

    # Live call to OpenWeatherMap with 5 second timeout
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": loc,
        "appid": api_key,
        "units": "metric",
    }

    try:
        resp = requests.get(url, params=params, timeout=5.0)
        if resp.status_code == 404:
            return {"error": f"Location '{loc}' was not found. Please verify the city name.", "status_code": 404}
        if resp.status_code == 401:
            return {"error": "Invalid Weather API key configured on server.", "status_code": 401}
        resp.raise_for_status()

        data = resp.json()
        main = data.get("main", {})
        weather_desc = data.get("weather", [{}])[0].get("description", "Clear").title()
        temp = float(main.get("temp", 25.0))
        humidity = int(main.get("humidity", 50))
        wind_speed_ms = float(data.get("wind", {}).get("speed", 3.0))
        wind_speed_kmh = round(wind_speed_ms * 3.6, 1)

        advisories = get_agricultural_weather_advisory(temp, humidity, weather_desc, wind_speed_kmh)

        return {
            "is_live": True,
            "provider": "OpenWeatherMap API",
            "notice": None,
            "location": f"{data.get('name')}, {data.get('sys', {}).get('country')}",
            "temperature_c": round(temp, 1),
            "humidity_percent": humidity,
            "wind_speed_kmh": wind_speed_kmh,
            "condition": weather_desc,
            "forecast_summary": f"{weather_desc} with temperature around {round(temp)}°C and {humidity}% humidity.",
            "advisories": advisories,
            "updated_at": "Live update",
        }

    except requests.exceptions.Timeout:
        return {"error": "Weather service connection timed out (exceeded 5s). Please try again.", "status_code": 504}
    except requests.exceptions.RequestException as e:
        return {"error": f"Unable to reach weather provider: {str(e)}", "status_code": 502}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}", "status_code": 500}

