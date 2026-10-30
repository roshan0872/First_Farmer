from flask import Blueprint, render_template, request
from app.services.weather import fetch_weather_for_location

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/weather")
def index():
    """Page 10 — Agricultural Weather Advisory."""
    location = request.args.get("location", "").strip() or "Coimbatore"
    weather_data = fetch_weather_for_location(location)

    return render_template(
        "weather/index.html",
        weather=weather_data,
        location=location,
    )
