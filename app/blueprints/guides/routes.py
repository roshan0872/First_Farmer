from flask import Blueprint, render_template, request
from app.models.crop import Crop, CultivationGuide, PestDisease, HarvestGuide, PostHarvestGuide, CropProduct
from app.services.i18n import get_current_language

guides_bp = Blueprint("guides", __name__)

@guides_bp.route("/cultivation")
def cultivation():
    """Page 6 (Top-Level) — Cultivation Guide with Crop Selector."""
    crop_slug = request.args.get("crop")
    crops = Crop.query.filter_by(is_published=True).order_by(Crop.name.asc()).all()

    selected_crop = None
    if crop_slug:
        selected_crop = Crop.query.filter((Crop.slug == crop_slug) | (Crop.id == crop_slug)).first()
    if not selected_crop and crops:
        selected_crop = crops[0]

    return render_template(
        "guides/cultivation.html",
        crops=crops,
        selected_crop=selected_crop,
    )


@guides_bp.route("/pests-diseases")
def pests_diseases():
    """Page 7 — Pest and Disease Guide (Educational, IPM focused)."""
    search = request.args.get("q", "").strip()
    crop_id = request.args.get("crop", type=int)
    item_type = request.args.get("type", "")

    crops = Crop.query.filter_by(is_published=True).order_by(Crop.name.asc()).all()
    query = PestDisease.query.join(Crop).filter(Crop.is_published == True)

    if crop_id:
        query = query.filter(PestDisease.crop_id == crop_id)

    if item_type in ["pest", "disease", "other"]:
        query = query.filter(PestDisease.type == item_type)

    if search:
        s_fmt = f"%{search}%"
        query = query.filter(
            (PestDisease.name.ilike(s_fmt)) |
            (PestDisease.symptoms.ilike(s_fmt)) |
            (PestDisease.prevention.ilike(s_fmt)) |
            (PestDisease.management.ilike(s_fmt))
        )

    records = query.order_by(PestDisease.name.asc()).all()

    return render_template(
        "guides/pests_diseases.html",
        crops=crops,
        records=records,
        search=search,
        selected_crop_id=crop_id,
        selected_type=item_type,
    )


@guides_bp.route("/harvest")
def harvest():
    """Page 8 — Harvesting Guide."""
    crop_slug = request.args.get("crop")
    crops = Crop.query.filter_by(is_published=True).order_by(Crop.name.asc()).all()

    selected_crop = None
    if crop_slug:
        selected_crop = Crop.query.filter((Crop.slug == crop_slug) | (Crop.id == crop_slug)).first()
    if not selected_crop and crops:
        selected_crop = crops[0]

    return render_template(
        "guides/harvest.html",
        crops=crops,
        selected_crop=selected_crop,
    )


@guides_bp.route("/post-harvest")
def post_harvest():
    """Page 9 — Post-Harvest and Value Addition (Key Educational Differentiator)."""
    crop_slug = request.args.get("crop")
    category = request.args.get("category", "")

    crops = Crop.query.filter_by(is_published=True).order_by(Crop.name.asc()).all()

    selected_crop = None
    if crop_slug:
        selected_crop = Crop.query.filter((Crop.slug == crop_slug) | (Crop.id == crop_slug)).first()
    if not selected_crop and crops:
        selected_crop = crops[0]

    # All value-added products catalog
    prod_query = CropProduct.query.join(Crop).filter(Crop.is_published == True)
    if selected_crop:
        prod_query = prod_query.filter(CropProduct.crop_id == selected_crop.id)
    if category:
        prod_query = prod_query.filter(CropProduct.product_category == category)

    products = prod_query.all()

    return render_template(
        "guides/post_harvest.html",
        crops=crops,
        selected_crop=selected_crop,
        products=products,
        category=category,
    )

