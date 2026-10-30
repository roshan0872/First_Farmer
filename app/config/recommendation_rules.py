# Rule Weights and Thresholds for Crop Recommendation
# Configured in a dedicated module to ensure maintainability and transparency.

CRITERIA_WEIGHTS = {
    "season": 30,
    "soil": 25,
    "water": 25,
    "region": 15,
    "climate": 5,  # Temperature and rainfall
}

# Score thresholds for classification
STRONG_MATCH_THRESHOLD = 75
MODERATE_MATCH_THRESHOLD = 50

# Water requirement compatibility matrix
# (crop_requirement, user_availability) -> (is_hard_conflict, score_fraction, explanation)
WATER_COMPATIBILITY = {
    ("High", "High"): (False, 1.0, "High water availability fully satisfies high crop irrigation demand."),
    ("High", "Medium"): (False, 0.5, "High water requirement can be partially met with strict water-saving methods like drip or AWD."),
    ("High", "Low"): (True, 0.0, "Crop requires high water, which severely conflicts with low water availability."),
    
    ("Medium", "High"): (False, 0.9, "Abundant water satisfies medium crop water needs (ensure adequate drainage to prevent waterlogging)."),
    ("Medium", "Medium"): (False, 1.0, "Medium water availability matches crop requirements well."),
    ("Medium", "Low"): (False, 0.4, "Medium crop can survive on low water only with supplemental micro-irrigation."),
    
    ("Low", "High"): (False, 0.7, "Crop tolerates low water; excess water requires very well-drained soils to avoid root rot."),
    ("Low", "Medium"): (False, 0.9, "Medium water availability is more than adequate for low-water drought-hardy crops."),
    ("Low", "Low"): (False, 1.0, "Low-water crop is perfectly adapted for dryland or water-deficit conditions."),
}

DISCLAIMER_TEXT = "Preliminary educational suggestion. Verify with local agricultural guidance and a soil test before making cultivation decisions."

