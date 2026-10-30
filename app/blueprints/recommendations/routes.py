from flask import Blueprint, render_template, request, g
from app.models.lookups import Region, SoilType, Season
from app.models.crop import FarmProfile
from app.forms import RecommendationForm
from app.services.recommendation import evaluate_crop_recommendation

recommendations_bp = Blueprint("recommendations", __name__)

@recommendations_bp.route("/recommendations", methods=["GET", "POST"])
def recommend():
    """Page 4 — Crop Recommendation Engine."""
    form = RecommendationForm()

    # Populate dynamic region choices
    regions = Region.query.order_by(Region.name.asc()).all()
    form.region.choices = [("", "Select Region / Agro-climatic Zone (Optional)")] + [
        (r.name, f"{r.name} ({r.zone or r.state})") for r in regions
    ]

    # Pre-populate if logged in and profile exists (on GET)
    if request.method == "GET" and g.current_user:
        profile = FarmProfile.query.filter_by(user_id=g.current_user.id).first()
        if profile:
            if profile.region:
                form.region.data = profile.region
            if profile.soil_type:
                form.soil_type.data = profile.soil_type
            if profile.season:
                form.season.data = profile.season
            if profile.water_availability:
                form.water_availability.data = profile.water_availability
            if profile.temperature is not None:
                form.temperature.data = profile.temperature
            if profile.rainfall is not None:
                form.rainfall.data = profile.rainfall

    results = None
    has_searched = False

    if form.validate_on_submit():
        has_searched = True
        user_id = g.current_user.id if g.current_user else None
        results = evaluate_crop_recommendation(
            soil_type=form.soil_type.data,
            season=form.season.data,
            water_availability=form.water_availability.data,
            region_name=form.region.data or None,
            temperature=form.temperature.data,
            rainfall=form.rainfall.data,
            preferred_category=form.preferred_category.data,
            user_id=user_id,
        )

    return render_template(
        "recommendations/recommend.html",
        form=form,
        results=results,
        has_searched=has_searched,
    )

