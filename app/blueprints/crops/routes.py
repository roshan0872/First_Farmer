from datetime import datetime, timezone
from flask import Blueprint, render_template, request, abort, g, redirect, url_for, flash
from app.extensions import db
from app.models.crop import Crop
from app.models.lookups import SoilType, Season
from app.models.learning import CropBookmark, CropView, LearningProgress, LearningModule
from app.services.i18n import get_entity_translation, get_current_language

crops_bp = Blueprint("crops", __name__)

@crops_bp.route("/crops")
def library():
    """Page 5 — Crop Learning Library (Search, Filter, Sort, Paginate)."""
    search_query = request.args.get("q", "").strip()
    selected_category = request.args.get("category", "")
    selected_soil = request.args.get("soil", "")
    selected_season = request.args.get("season", "")
    selected_water = request.args.get("water", "")
    sort_order = request.args.get("sort", "az")
    page = request.args.get("page", 1, type=int)

    query = Crop.query.filter_by(is_published=True)

    # Search filter
    if search_query:
        search_fmt = f"%{search_query}%"
        query = query.filter(
            (Crop.name.ilike(search_fmt)) |
            (Crop.scientific_name.ilike(search_fmt)) |
            (Crop.description.ilike(search_fmt))
        )

    # Category filter
    if selected_category:
        query = query.filter_by(category=selected_category)

    # Water requirement filter
    if selected_water:
        query = query.filter_by(water_requirement=selected_water)

    # Soil filter (via junction)
    if selected_soil:
        query = query.filter(Crop.soils.any(SoilType.name == selected_soil))

    # Season filter (via junction)
    if selected_season:
        query = query.filter(Crop.seasons.any(Season.name == selected_season))

    # Sort
    if sort_order == "za":
        query = query.order_by(Crop.name.desc())
    else:
        query = query.order_by(Crop.name.asc())

    pagination = query.paginate(page=page, per_page=6, error_out=False)

    # Collect bookmarked crop IDs for active user
    bookmarked_ids = set()
    if g.current_user:
        bmarks = CropBookmark.query.filter_by(user_id=g.current_user.id).all()
        bookmarked_ids = {b.crop_id for b in bmarks}

    all_soils = SoilType.query.all()
    all_seasons = Season.query.all()
    categories = ["Cereal", "Pulse", "Vegetable", "Fruit", "Cash Crop", "Millets"]

    return render_template(
        "crops/library.html",
        pagination=pagination,
        crops=pagination.items,
        search_query=search_query,
        selected_category=selected_category,
        selected_soil=selected_soil,
        selected_season=selected_season,
        selected_water=selected_water,
        sort_order=sort_order,
        all_soils=all_soils,
        all_seasons=all_seasons,
        categories=categories,
        bookmarked_ids=bookmarked_ids,
    )


@crops_bp.route("/crops/<slug>")
def detail(slug):
    """Page 6 — Crop Detail and Complete Cultivation Guide."""
    crop = Crop.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Track recently viewed
    if g.current_user:
        view = CropView.query.filter_by(user_id=g.current_user.id, crop_id=crop.id).first()
        if not view:
            view = CropView(user_id=g.current_user.id, crop_id=crop.id)
            db.session.add(view)
        else:
            view.viewed_at = datetime.now(timezone.utc)
        db.session.commit()

    # Check if bookmarked
    is_bookmarked = False
    module_completed = False
    if g.current_user:
        is_bookmarked = CropBookmark.query.filter_by(user_id=g.current_user.id, crop_id=crop.id).first() is not None
        if crop.learning_module:
            lp = LearningProgress.query.filter_by(user_id=g.current_user.id, learning_module_id=crop.learning_module.id).first()
            if lp and lp.completion_status == "completed":
                module_completed = True

    # Check multilingual content availability
    lang = get_current_language()
    translated_name, is_name_tr = get_entity_translation("crop", crop.id, "name", lang)
    translated_desc, is_desc_tr = get_entity_translation("crop", crop.id, "description", lang)

    has_translation = is_name_tr and is_desc_tr

    return render_template(
        "crops/detail.html",
        crop=crop,
        is_bookmarked=is_bookmarked,
        module_completed=module_completed,
        translated_name=translated_name or crop.name,
        translated_desc=translated_desc or crop.description,
        has_translation=has_translation,
        current_lang=lang,
    )

