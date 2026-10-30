from app.models.crop import Crop, FarmProfile
from app.models.lookups import SoilType, Season, Region
from app.extensions import db
from app.config.recommendation_rules import (
    CRITERIA_WEIGHTS,
    STRONG_MATCH_THRESHOLD,
    MODERATE_MATCH_THRESHOLD,
    WATER_COMPATIBILITY,
    DISCLAIMER_TEXT,
)

def evaluate_crop_recommendation(
    soil_type: str,
    season: str,
    water_availability: str,
    region_name: str | None = None,
    temperature: float | None = None,
    rainfall: float | None = None,
    preferred_category: str | None = None,
    user_id: int | None = None,
) -> dict:
    """
    Evaluates published crops against user farming conditions and computes a transparent,
    weighted match score with explanations.
    """
    # 1. Save or update FarmProfile if user_id is provided
    if user_id:
        profile = FarmProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = FarmProfile(user_id=user_id)
            db.session.add(profile)
        profile.soil_type = soil_type
        profile.season = season
        profile.water_availability = water_availability
        profile.region = region_name
        profile.temperature = temperature
        profile.rainfall = rainfall
        db.session.commit()

    # 2. Check missing optional fields to adjust weights fairly
    missing_fields = []
    active_weights = dict(CRITERIA_WEIGHTS)

    if not region_name:
        missing_fields.append("Region / State")
        active_weights["region"] = 0

    if temperature is None and rainfall is None:
        missing_fields.append("Temperature & Rainfall")
        active_weights["climate"] = 0

    # Normalize weights so active criteria sum to 100
    total_active = sum(active_weights.values())
    if total_active > 0:
        norm_factor = 100.0 / total_active
    else:
        norm_factor = 1.0

    # 3. Fetch published crops with relationships
    query = Crop.query.filter_by(is_published=True)
    if preferred_category and preferred_category != "All":
        query = query.filter_by(category=preferred_category)
    crops = query.all()

    ranked_crops = []

    for crop in crops:
        matched_criteria = []
        conflicts = []
        explanations = []
        raw_score = 0.0

        # A. Season Check
        crop_seasons = [s.name for s in crop.seasons]
        is_perennial = "Year-round" in crop_seasons

        if season in crop_seasons or is_perennial:
            score_contribution = active_weights["season"] * norm_factor
            raw_score += score_contribution
            if is_perennial and season not in crop_seasons:
                matched_criteria.append(f"Perennial crop suitable throughout the year including {season}")
                explanations.append(f"Adapted as a multi-season perennial crop yielding across {season}.")
            else:
                matched_criteria.append(f"Matches primary growing season ({season})")
                explanations.append(f"Thrives during the {season} cultivation window.")
        else:
            conflicts.append(f"Season mismatch: Typically grown in {', '.join(crop_seasons)} rather than {season}")
            # If severe season mismatch and not perennial, exclude or penalize heavily
            explanations.append(f"Crop cycle does not align well with {season} season.")
            # Strict conflict exclusion
            continue

        # B. Water Availability Check
        water_pair = (crop.water_requirement, water_availability)
        is_hard_conflict, water_fraction, water_expl = WATER_COMPATIBILITY.get(
            water_pair, (False, 0.5, "Moderate water compatibility.")
        )

        if is_hard_conflict:
            # Exclude crop due to water shortage
            continue

        water_score = active_weights["water"] * norm_factor * water_fraction
        raw_score += water_score
        explanations.append(water_expl)

        if water_fraction >= 0.9:
            matched_criteria.append(f"Water requirement ({crop.water_requirement}) fits available water ({water_availability})")
        else:
            conflicts.append(f"Water stress risk: Crop requires {crop.water_requirement} water vs {water_availability} availability")

        # C. Soil Type Check
        crop_soils = [s.name for s in crop.soils]
        if soil_type in crop_soils:
            soil_score = active_weights["soil"] * norm_factor
            raw_score += soil_score
            matched_criteria.append(f"Soil suitability ({soil_type} is an optimal soil for {crop.name})")
            explanations.append(f"Roots and drainage perform well in {soil_type} soil.")
        else:
            conflicts.append(f"Suboptimal soil: Prefers {', '.join(crop_soils)} instead of {soil_type}")
            explanations.append(f"{soil_type} soil may require soil conditioning (organic matter/drainage) for optimal growth.")

        # D. Region Check (if provided)
        if region_name and active_weights["region"] > 0:
            crop_regions = [r.name for r in crop.regions]
            if any(region_name.lower() in r.lower() or r.lower() in region_name.lower() for r in crop_regions):
                raw_score += active_weights["region"] * norm_factor
                matched_criteria.append(f"Adapted to {region_name}")
                explanations.append(f"Demonstrated field track record in {region_name}.")
            else:
                conflicts.append(f"Not traditionally categorized under {region_name} primary zones")

        # E. Climate Check (if temperature or rainfall provided)
        if active_weights["climate"] > 0:
            climate_matched = True
            if temperature is not None:
                if crop.min_temp and crop.max_temp:
                    if crop.min_temp <= temperature <= crop.max_temp:
                        matched_criteria.append(f"Temperature ({temperature}°C) within ideal band ({crop.min_temp}-{crop.max_temp}°C)")
                    else:
                        climate_matched = False
                        conflicts.append(f"Temperature {temperature}°C outside optimal {crop.min_temp}-{crop.max_temp}°C")
            if rainfall is not None:
                if crop.min_rainfall and crop.max_rainfall:
                    if crop.min_rainfall <= rainfall <= crop.max_rainfall:
                        matched_criteria.append(f"Rainfall ({rainfall} mm) within typical range ({crop.min_rainfall}-{crop.max_rainfall} mm)")
                    else:
                        climate_matched = False
                        conflicts.append(f"Rainfall {rainfall} mm diverges from preferred range")

            if climate_matched:
                raw_score += active_weights["climate"] * norm_factor

        # Round final score
        final_score = min(100, int(round(raw_score)))

        # Categorize
        if final_score >= STRONG_MATCH_THRESHOLD:
            category_label = "Strong match"
        elif final_score >= MODERATE_MATCH_THRESHOLD:
            category_label = "Moderate match"
        else:
            category_label = "Weak match"

        ranked_crops.append({
            "crop": crop,
            "score": final_score,
            "match_category": category_label,
            "matched_criteria": matched_criteria,
            "conflicts": conflicts,
            "missing_info": missing_fields,
            "explanation": " ".join(explanations),
        })

    # Sort descending by score
    ranked_crops.sort(key=lambda x: x["score"], reverse=True)

    strong_matches = [c for c in ranked_crops if c["match_category"] == "Strong match"]
    moderate_matches = [c for c in ranked_crops if c["match_category"] == "Moderate match"]
    weak_matches = [c for c in ranked_crops if c["match_category"] == "Weak match"]

    return {
        "disclaimer": DISCLAIMER_TEXT,
        "total_results": len(ranked_crops),
        "strong_matches": strong_matches,
        "moderate_matches": moderate_matches,
        "weak_matches": weak_matches,
        "all_ranked": ranked_crops,
        "missing_fields": missing_fields,
        "inputs": {
            "soil_type": soil_type,
            "season": season,
            "water_availability": water_availability,
            "region": region_name,
            "temperature": temperature,
            "rainfall": rainfall,
        }
    }

