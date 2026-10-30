from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, session, g
from app.extensions import db, hash_password, verify_password
from app.models.user import User
from app.models.crop import (
    Crop,
    CultivationGuide,
    PestDisease,
    HarvestGuide,
    PostHarvestGuide,
    CropProduct,
)
from app.models.learning import CropBookmark, LearningProgress, LearningModule
from app.models.interactions import ChatMessage
from app.services.security import (
    login_required,
    admin_required,
    is_login_locked,
    record_login_failure,
    clear_login_attempts,
)
from app.services.recommendation import evaluate_crop_recommendation
from app.services.weather import fetch_weather_for_location
from app.services.chatbot import ChatbotService

api_bp = Blueprint("api", __name__, url_prefix="/api")

# --- Authentication API ---
@api_bp.route("/auth/me", methods=["GET"])
def auth_me():
    if not g.current_user:
        return jsonify({"authenticated": False, "user": None}), 200
    return jsonify({"authenticated": True, "user": g.current_user.to_dict()}), 200


@api_bp.route("/auth/register", methods=["POST"])
def auth_register():
    data = request.get_json(silent=True) or request.form
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    lang = data.get("preferred_language", "en")

    if not full_name or not email or not password:
        return jsonify({"error": "Missing required fields: full_name, email, password"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email is already registered"}), 409

    user = User(
        full_name=full_name,
        email=email,
        password_hash=hash_password(password),
        role="student",
        preferred_language=lang if lang in ["en", "ta", "hi"] else "en",
    )
    db.session.add(user)
    db.session.commit()

    session.clear()
    session["user_id"] = user.id
    session["lang"] = user.preferred_language

    return jsonify({"success": True, "user": user.to_dict()}), 201


@api_bp.route("/auth/login", methods=["POST"])
def auth_login():
    data = request.get_json(silent=True) or request.form
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    if is_login_locked(email):
        return jsonify({"error": "Too many failed attempts. Please try again in 5 minutes."}), 429

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(user.password_hash, password):
        record_login_failure(email)
        return jsonify({"error": "The email or password you entered is incorrect. Please try again."}), 401

    clear_login_attempts(email)
    session.clear()
    session["user_id"] = user.id
    session["lang"] = user.preferred_language

    return jsonify({"success": True, "user": user.to_dict()}), 200


@api_bp.route("/auth/logout", methods=["POST"])
def auth_logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"}), 200


@api_bp.route("/auth/change-password", methods=["POST"])
@login_required
def auth_change_password():
    data = request.get_json(silent=True) or request.form
    curr = data.get("current_password", "")
    new_p = data.get("new_password", "")

    if not curr or not new_p:
        return jsonify({"error": "Missing current_password or new_password"}), 400

    if len(new_p) < 8:
        return jsonify({"error": "New password must be at least 8 characters"}), 400

    if not verify_password(g.current_user.password_hash, curr):
        return jsonify({"error": "Current password is incorrect"}), 400

    g.current_user.password_hash = hash_password(new_p)
    db.session.commit()
    return jsonify({"success": True, "message": "Password updated successfully"}), 200


# --- Crops API ---
@api_bp.route("/crops", methods=["GET"])
def api_crops_list():
    category = request.args.get("category")
    water = request.args.get("water")
    q = request.args.get("q")
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 50)

    query = Crop.query.filter_by(is_published=True)
    if category:
        query = query.filter_by(category=category)
    if water:
        query = query.filter_by(water_requirement=water)
    if q:
        query = query.filter(Crop.name.ilike(f"%{q}%"))

    pagination = query.order_by(Crop.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "items": [c.to_dict() for c in pagination.items],
    }), 200


@api_bp.route("/crops/<int:id>", methods=["GET"])
def api_crop_get(id):
    crop = db.get_or_404(Crop, id)
    return jsonify(crop.to_dict()), 200


@api_bp.route("/crops", methods=["POST"])
@admin_required
def api_crop_create():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    slug = data.get("slug", "").strip()
    category = data.get("category", "")
    description = data.get("description", "")
    water = data.get("water_requirement", "Medium")

    if not name or not slug or not category or not description:
        return jsonify({"error": "Missing required fields: name, slug, category, description"}), 400

    if Crop.query.filter_by(slug=slug).first():
        return jsonify({"error": "Slug already in use"}), 409

    crop = Crop(
        name=name,
        slug=slug,
        scientific_name=data.get("scientific_name"),
        category=category,
        description=description,
        water_requirement=water,
        season_summary=data.get("season_summary"),
        soil_climate_summary=data.get("soil_climate_summary"),
        image_path=data.get("image_path", "/static/img/crop-placeholder.svg"),
        min_temp=data.get("min_temp"),
        max_temp=data.get("max_temp"),
        min_rainfall=data.get("min_rainfall"),
        max_rainfall=data.get("max_rainfall"),
        difficulty_level=data.get("difficulty_level", "Beginner"),
        is_published=data.get("is_published", True),
    )
    db.session.add(crop)
    db.session.commit()
    return jsonify(crop.to_dict()), 201


@api_bp.route("/crops/<int:id>", methods=["PUT"])
@admin_required
def api_crop_update(id):
    crop = db.get_or_404(Crop, id)
    data = request.get_json(silent=True) or {}
    for key in ["name", "scientific_name", "category", "description", "water_requirement", "season_summary", "soil_climate_summary", "image_path", "difficulty_level"]:
        if key in data:
            setattr(crop, key, data[key])
    if "is_published" in data:
        crop.is_published = bool(data["is_published"])
    db.session.commit()
    return jsonify(crop.to_dict()), 200


@api_bp.route("/crops/<int:id>", methods=["DELETE"])
@admin_required
def api_crop_delete(id):
    crop = db.get_or_404(Crop, id)
    db.session.delete(crop)
    db.session.commit()
    return jsonify({"success": True, "message": "Crop deleted"}), 200


# --- Guides API ---
@api_bp.route("/crops/<int:id>/cultivation", methods=["GET"])
def api_cultivation_guide(id):
    crop = db.get_or_404(Crop, id)
    if not crop.cultivation_guide:
        return jsonify({"error": "No cultivation guide for this crop"}), 404
    g = crop.cultivation_guide
    return jsonify({
        "crop_id": crop.id,
        "crop_name": crop.name,
        "seed_selection": g.seed_selection,
        "land_preparation": g.land_preparation,
        "sowing_method": g.sowing_method,
        "irrigation": g.irrigation,
        "nutrient_management": g.nutrient_management,
        "weed_management": g.weed_management,
        "growth_stages": g.growth_stages,
        "common_mistakes": g.common_mistakes,
        "source_reference": g.source_reference,
        "last_reviewed_at": g.last_reviewed_at,
    }), 200


@api_bp.route("/crops/<int:id>/pests-diseases", methods=["GET"])
def api_pests_guide(id):
    crop = db.get_or_404(Crop, id)
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "type": p.type,
        "symptoms": p.symptoms,
        "contributing_conditions": p.contributing_conditions,
        "prevention": p.prevention,
        "management": p.management,
        "source_reference": p.source_reference,
        "last_reviewed_at": p.last_reviewed_at,
    } for p in crop.pests_diseases]), 200


@api_bp.route("/crops/<int:id>/harvest", methods=["GET"])
def api_harvest_guide(id):
    crop = db.get_or_404(Crop, id)
    if not crop.harvest_guide:
        return jsonify({"error": "No harvest guide for this crop"}), 404
    h = crop.harvest_guide
    return jsonify({
        "crop_id": crop.id,
        "crop_name": crop.name,
        "maturity_indicators": h.maturity_indicators,
        "approximate_harvest_period": h.approximate_harvest_period,
        "harvesting_method": h.harvesting_method,
        "handling_precautions": h.handling_precautions,
        "storage_preparation": h.storage_preparation,
        "source_reference": h.source_reference,
        "last_reviewed_at": h.last_reviewed_at,
    }), 200


@api_bp.route("/crops/<int:id>/post-harvest", methods=["GET"])
def api_post_harvest_guide(id):
    crop = db.get_or_404(Crop, id)
    if not crop.post_harvest_guide:
        return jsonify({"error": "No post-harvest guide for this crop"}), 404
    ph = crop.post_harvest_guide
    return jsonify({
        "crop_id": crop.id,
        "crop_name": crop.name,
        "cleaning_and_grading": ph.cleaning_and_grading,
        "storage_method": ph.storage_method,
        "preservation_method": ph.preservation_method,
        "processing_method": ph.processing_method,
        "packaging_method": ph.packaging_method,
        "food_uses": ph.food_uses,
        "industrial_uses": ph.industrial_uses,
        "by_products": ph.by_products,
        "source_reference": ph.source_reference,
        "last_reviewed_at": ph.last_reviewed_at,
    }), 200


@api_bp.route("/crops/<int:id>/products", methods=["GET"])
def api_products_guide(id):
    crop = db.get_or_404(Crop, id)
    return jsonify([{
        "id": p.id,
        "product_name": p.product_name,
        "product_category": p.product_category,
        "raw_material": p.raw_material,
        "processing_overview": p.processing_overview,
        "common_uses": p.common_uses,
        "storage_considerations": p.storage_considerations,
        "value_addition_notes": p.value_addition_notes,
    } for p in crop.products]), 200


# --- Recommendations API ---
@api_bp.route("/recommendations", methods=["POST"])
def api_recommend():
    data = request.get_json(silent=True) or request.form
    soil_type = data.get("soil_type")
    season = data.get("season")
    water = data.get("water_availability")

    if not soil_type or not season or not water:
        return jsonify({"error": "Missing required fields: soil_type, season, water_availability"}), 400

    user_id = g.current_user.id if g.current_user else None
    results = evaluate_crop_recommendation(
        soil_type=soil_type,
        season=season,
        water_availability=water,
        region_name=data.get("region"),
        temperature=float(data["temperature"]) if data.get("temperature") else None,
        rainfall=float(data["rainfall"]) if data.get("rainfall") else None,
        preferred_category=data.get("preferred_category"),
        user_id=user_id,
    )

    # Serialize ranked crop objects
    serialized_results = []
    for item in results["all_ranked"]:
        serialized_results.append({
            "crop": item["crop"].to_dict(),
            "score": item["score"],
            "match_category": item["match_category"],
            "matched_criteria": item["matched_criteria"],
            "conflicts": item["conflicts"],
            "explanation": item["explanation"],
        })

    return jsonify({
        "disclaimer": results["disclaimer"],
        "total_results": results["total_results"],
        "ranked_crops": serialized_results,
        "missing_fields": results["missing_fields"],
    }), 200


# --- Bookmarks & Progress API ---
@api_bp.route("/bookmarks", methods=["GET"])
@login_required
def api_bookmarks_list():
    bms = CropBookmark.query.filter_by(user_id=g.current_user.id).all()
    return jsonify([b.crop.to_dict() for b in bms]), 200


@api_bp.route("/bookmarks/<int:crop_id>", methods=["POST"])
@login_required
def api_bookmark_add(crop_id):
    crop = db.get_or_404(Crop, crop_id)
    existing = CropBookmark.query.filter_by(user_id=g.current_user.id, crop_id=crop.id).first()
    if existing:
        return jsonify({"bookmarked": True, "message": "Already bookmarked"}), 200
    bm = CropBookmark(user_id=g.current_user.id, crop_id=crop.id)
    db.session.add(bm)
    db.session.commit()
    return jsonify({"bookmarked": True, "message": f"Saved {crop.name}"}), 201


@api_bp.route("/bookmarks/<int:crop_id>", methods=["DELETE"])
@login_required
def api_bookmark_remove(crop_id):
    bm = CropBookmark.query.filter_by(user_id=g.current_user.id, crop_id=crop_id).first()
    if bm:
        db.session.delete(bm)
        db.session.commit()
    return jsonify({"bookmarked": False, "message": "Removed bookmark"}), 200


@api_bp.route("/progress", methods=["GET"])
@login_required
def api_progress_get():
    records = LearningProgress.query.filter_by(user_id=g.current_user.id).all()
    return jsonify([{
        "module_id": r.learning_module_id,
        "module_slug": r.module.slug if r.module else None,
        "completion_status": r.completion_status,
        "progress_percentage": r.progress_percentage,
    } for r in records]), 200


@api_bp.route("/progress/<int:module_id>", methods=["POST"])
@login_required
def api_progress_update(module_id):
    module = db.get_or_404(LearningModule, module_id)
    data = request.get_json(silent=True) or {}
    status = data.get("status", "completed")

    progress = LearningProgress.query.filter_by(user_id=g.current_user.id, learning_module_id=module.id).first()
    if not progress:
        progress = LearningProgress(user_id=g.current_user.id, learning_module_id=module.id)
        db.session.add(progress)

    progress.completion_status = status
    progress.progress_percentage = 100 if status == "completed" else 50
    progress.last_accessed_at = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"success": True, "status": progress.completion_status, "percentage": progress.progress_percentage}), 200


# --- Weather API ---
@api_bp.route("/weather", methods=["GET"])
def api_weather():
    loc = request.args.get("location", "").strip() or "Coimbatore"
    data = fetch_weather_for_location(loc)
    return jsonify(data), 200


# --- Chatbot API ---
@api_bp.route("/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or request.form
    message = data.get("message", "").strip()
    conv_id = data.get("conversation_id") or session.get("conv_id") or "guest-conv"
    lang = data.get("lang") or session.get("lang") or "en"

    if not message:
        return jsonify({"error": "Empty message"}), 400

    user_id = g.current_user.id if g.current_user else None
    response = ChatbotService.query(user_id=user_id, message=message, conversation_id=conv_id, lang=lang)
    return jsonify(response), 200


@api_bp.route("/chat/history", methods=["DELETE"])
@login_required
def api_chat_clear():
    ChatMessage.query.filter_by(user_id=g.current_user.id).delete()
    db.session.commit()
    return jsonify({"success": True, "message": "Chat history cleared"}), 200
