from flask import Blueprint, render_template, request, redirect, url_for, flash, g, abort
from app.extensions import db
from app.models.crop import (
    Crop,
    CultivationGuide,
    PestDisease,
    HarvestGuide,
    PostHarvestGuide,
    CropProduct,
)
from app.models.learning import LearningModule, QuizQuestion
from app.models.interactions import Translation
from app.models.user import User, ActivityLog
from app.forms import AdminCropForm
from app.services.security import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def log_admin_activity(action: str, entity_type: str, entity_id: int | None = None):
    log = ActivityLog(
        user_id=g.current_user.id if g.current_user else None,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
    )
    db.session.add(log)
    db.session.commit()


@admin_bp.route("/")
@admin_required
def index():
    """Page 14 — Admin Dashboard Overview."""
    crops_count = Crop.query.count()
    users_count = User.query.count()
    pests_count = PestDisease.query.count()
    products_count = CropProduct.query.count()
    recent_logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(15).all()

    return render_template(
        "admin/index.html",
        crops_count=crops_count,
        users_count=users_count,
        pests_count=pests_count,
        products_count=products_count,
        recent_logs=recent_logs,
    )


# --- Crops Management ---
@admin_bp.route("/crops")
@admin_required
def crops_list():
    crops = Crop.query.order_by(Crop.name.asc()).all()
    return render_template("admin/crops_list.html", crops=crops)


@admin_bp.route("/crops/new", methods=["GET", "POST"])
@admin_required
def crop_create():
    form = AdminCropForm()
    if form.validate_on_submit():
        existing = Crop.query.filter_by(slug=form.slug.data.strip()).first()
        if existing:
            form.slug.errors.append("This slug is already in use.")
            return render_template("admin/crop_form.html", form=form, title="Create New Crop")

        crop = Crop(
            name=form.name.data.strip(),
            slug=form.slug.data.strip(),
            scientific_name=form.scientific_name.data.strip() if form.scientific_name.data else None,
            category=form.category.data,
            description=form.description.data.strip(),
            water_requirement=form.water_requirement.data,
            season_summary=form.season_summary.data.strip() if form.season_summary.data else None,
            soil_climate_summary=form.soil_climate_summary.data.strip() if form.soil_climate_summary.data else None,
            image_path=form.image_path.data.strip() if form.image_path.data else "/static/img/crop-placeholder.svg",
            min_temp=form.min_temp.data,
            max_temp=form.max_temp.data,
            min_rainfall=form.min_rainfall.data,
            max_rainfall=form.max_rainfall.data,
            difficulty_level=form.difficulty_level.data,
            is_published=form.is_published.data,
        )
        db.session.add(crop)
        db.session.commit()
        log_admin_activity("Created crop", "Crop", crop.id)
        flash(f"Crop '{crop.name}' created successfully.", "success")
        return redirect(url_for("admin.crops_list"))

    return render_template("admin/crop_form.html", form=form, title="Create New Crop")


@admin_bp.route("/crops/<int:id>/edit", methods=["GET", "POST"])
@admin_required
def crop_edit(id):
    crop = db.get_or_404(Crop, id)
    form = AdminCropForm(obj=crop)

    if form.validate_on_submit():
        crop.name = form.name.data.strip()
        crop.scientific_name = form.scientific_name.data.strip() if form.scientific_name.data else None
        crop.category = form.category.data
        crop.description = form.description.data.strip()
        crop.water_requirement = form.water_requirement.data
        crop.season_summary = form.season_summary.data.strip() if form.season_summary.data else None
        crop.soil_climate_summary = form.soil_climate_summary.data.strip() if form.soil_climate_summary.data else None
        crop.image_path = form.image_path.data.strip() if form.image_path.data else crop.image_path
        crop.min_temp = form.min_temp.data
        crop.max_temp = form.max_temp.data
        crop.min_rainfall = form.min_rainfall.data
        crop.max_rainfall = form.max_rainfall.data
        crop.difficulty_level = form.difficulty_level.data
        crop.is_published = form.is_published.data

        db.session.commit()
        log_admin_activity("Updated crop", "Crop", crop.id)
        flash(f"Crop '{crop.name}' updated successfully.", "success")
        return redirect(url_for("admin.crops_list"))

    return render_template("admin/crop_form.html", form=form, title=f"Edit Crop: {crop.name}")


@admin_bp.route("/crops/<int:id>/delete", methods=["GET", "POST"])
@admin_required
def crop_delete(id):
    """Destructive action with confirmation fallback."""
    crop = db.get_or_404(Crop, id)

    if request.method == "POST":
        name = crop.name
        db.session.delete(crop)
        db.session.commit()
        log_admin_activity("Deleted crop", "Crop", id)
        flash(f"Crop '{name}' has been permanently deleted.", "info")
        return redirect(url_for("admin.crops_list"))

    # GET confirmation page (no-JS fallback)
    return render_template(
        "admin/confirm_delete.html",
        title="Confirm Delete Crop",
        item_name=crop.name,
        back_url=url_for("admin.crops_list"),
    )


# --- Guides Management ---
@admin_bp.route("/crops/<int:id>/guides", methods=["GET", "POST"])
@admin_required
def guides_edit(id):
    crop = db.get_or_404(Crop, id)
    cult = crop.cultivation_guide
    harvest = crop.harvest_guide
    post_harvest = crop.post_harvest_guide

    if request.method == "POST":
        guide_type = request.form.get("guide_type")

        if guide_type == "cultivation":
            if not cult:
                cult = CultivationGuide(crop_id=crop.id)
                db.session.add(cult)
            cult.seed_selection = request.form.get("seed_selection", "")
            cult.land_preparation = request.form.get("land_preparation", "")
            cult.sowing_method = request.form.get("sowing_method", "")
            cult.irrigation = request.form.get("irrigation", "")
            cult.nutrient_management = request.form.get("nutrient_management", "")
            cult.weed_management = request.form.get("weed_management", "")
            cult.growth_stages = request.form.get("growth_stages", "")
            cult.common_mistakes = request.form.get("common_mistakes", "")
            cult.source_reference = request.form.get("source_reference", "")
            cult.last_reviewed_at = request.form.get("last_reviewed_at", "")
            flash("Cultivation guide updated.", "success")

        elif guide_type == "harvest":
            if not harvest:
                harvest = HarvestGuide(crop_id=crop.id)
                db.session.add(harvest)
            harvest.maturity_indicators = request.form.get("maturity_indicators", "")
            harvest.approximate_harvest_period = request.form.get("approximate_harvest_period", "")
            harvest.harvesting_method = request.form.get("harvesting_method", "")
            harvest.handling_precautions = request.form.get("handling_precautions", "")
            harvest.storage_preparation = request.form.get("storage_preparation", "")
            harvest.source_reference = request.form.get("source_reference", "")
            harvest.last_reviewed_at = request.form.get("last_reviewed_at", "")
            flash("Harvest guide updated.", "success")

        elif guide_type == "post_harvest":
            if not post_harvest:
                post_harvest = PostHarvestGuide(crop_id=crop.id)
                db.session.add(post_harvest)
            post_harvest.cleaning_and_grading = request.form.get("cleaning_and_grading", "")
            post_harvest.storage_method = request.form.get("storage_method", "")
            post_harvest.preservation_method = request.form.get("preservation_method", "")
            post_harvest.processing_method = request.form.get("processing_method", "")
            post_harvest.packaging_method = request.form.get("packaging_method", "")
            post_harvest.food_uses = request.form.get("food_uses", "")
            post_harvest.industrial_uses = request.form.get("industrial_uses", "")
            post_harvest.by_products = request.form.get("by_products", "")
            post_harvest.source_reference = request.form.get("source_reference", "")
            post_harvest.last_reviewed_at = request.form.get("last_reviewed_at", "")
            flash("Post-harvest guide updated.", "success")

        db.session.commit()
        log_admin_activity(f"Updated {guide_type} guide", "Guide", crop.id)
        return redirect(url_for("admin.guides_edit", id=crop.id))

    return render_template(
        "admin/guides_edit.html",
        crop=crop,
        cult=cult,
        harvest=harvest,
        post_harvest=post_harvest,
    )


# --- Pests & Diseases Management ---
@admin_bp.route("/pests")
@admin_required
def pests_list():
    pests = PestDisease.query.order_by(PestDisease.name.asc()).all()
    return render_template("admin/pests_list.html", pests=pests)


@admin_bp.route("/pests/new", methods=["GET", "POST"])
@admin_required
def pest_create():
    crops = Crop.query.order_by(Crop.name.asc()).all()
    if request.method == "POST":
        p = PestDisease(
            crop_id=int(request.form.get("crop_id")),
            name=request.form.get("name", "").strip(),
            type=request.form.get("type", "pest"),
            symptoms=request.form.get("symptoms", "").strip(),
            contributing_conditions=request.form.get("contributing_conditions", "").strip(),
            prevention=request.form.get("prevention", "").strip(),
            management=request.form.get("management", "").strip(),
            source_reference=request.form.get("source_reference", "").strip(),
            last_reviewed_at=request.form.get("last_reviewed_at", "").strip(),
        )
        db.session.add(p)
        db.session.commit()
        log_admin_activity("Created pest/disease entry", "PestDisease", p.id)
        flash(f"Pest record '{p.name}' created.", "success")
        return redirect(url_for("admin.pests_list"))

    return render_template("admin/pest_form.html", crops=crops, pest=None, title="Add Pest / Disease")


@admin_bp.route("/pests/<int:id>/edit", methods=["GET", "POST"])
@admin_required
def pest_edit(id):
    p = db.get_or_404(PestDisease, id)
    crops = Crop.query.order_by(Crop.name.asc()).all()
    if request.method == "POST":
        p.crop_id = int(request.form.get("crop_id"))
        p.name = request.form.get("name", "").strip()
        p.type = request.form.get("type", "pest")
        p.symptoms = request.form.get("symptoms", "").strip()
        p.contributing_conditions = request.form.get("contributing_conditions", "").strip()
        p.prevention = request.form.get("prevention", "").strip()
        p.management = request.form.get("management", "").strip()
        p.source_reference = request.form.get("source_reference", "").strip()
        p.last_reviewed_at = request.form.get("last_reviewed_at", "").strip()

        db.session.commit()
        log_admin_activity("Updated pest/disease entry", "PestDisease", p.id)
        flash(f"Pest record '{p.name}' updated.", "success")
        return redirect(url_for("admin.pests_list"))

    return render_template("admin/pest_form.html", crops=crops, pest=p, title=f"Edit Pest: {p.name}")


@admin_bp.route("/pests/<int:id>/delete", methods=["GET", "POST"])
@admin_required
def pest_delete(id):
    p = db.get_or_404(PestDisease, id)
    if request.method == "POST":
        name = p.name
        db.session.delete(p)
        db.session.commit()
        log_admin_activity("Deleted pest/disease entry", "PestDisease", id)
        flash(f"Record '{name}' deleted.", "info")
        return redirect(url_for("admin.pests_list"))

    return render_template(
        "admin/confirm_delete.html",
        title="Confirm Delete Pest/Disease",
        item_name=p.name,
        back_url=url_for("admin.pests_list"),
    )


# --- Products Management ---
@admin_bp.route("/products")
@admin_required
def products_list():
    products = CropProduct.query.order_by(CropProduct.product_name.asc()).all()
    return render_template("admin/products_list.html", products=products)


@admin_bp.route("/products/new", methods=["GET", "POST"])
@admin_required
def product_create():
    crops = Crop.query.order_by(Crop.name.asc()).all()
    if request.method == "POST":
        pr = CropProduct(
            crop_id=int(request.form.get("crop_id")),
            product_name=request.form.get("product_name", "").strip(),
            product_category=request.form.get("product_category", "Food Product"),
            raw_material=request.form.get("raw_material", "").strip(),
            processing_overview=request.form.get("processing_overview", "").strip(),
            common_uses=request.form.get("common_uses", "").strip(),
            storage_considerations=request.form.get("storage_considerations", "").strip(),
            value_addition_notes=request.form.get("value_addition_notes", "").strip(),
        )
        db.session.add(pr)
        db.session.commit()
        log_admin_activity("Created product entry", "CropProduct", pr.id)
        flash(f"Product '{pr.product_name}' created.", "success")
        return redirect(url_for("admin.products_list"))

    return render_template("admin/product_form.html", crops=crops, product=None, title="Add Value-Added Product")


@admin_bp.route("/products/<int:id>/edit", methods=["GET", "POST"])
@admin_required
def product_edit(id):
    pr = db.get_or_404(CropProduct, id)
    crops = Crop.query.order_by(Crop.name.asc()).all()
    if request.method == "POST":
        pr.crop_id = int(request.form.get("crop_id"))
        pr.product_name = request.form.get("product_name", "").strip()
        pr.product_category = request.form.get("product_category", "Food Product")
        pr.raw_material = request.form.get("raw_material", "").strip()
        pr.processing_overview = request.form.get("processing_overview", "").strip()
        pr.common_uses = request.form.get("common_uses", "").strip()
        pr.storage_considerations = request.form.get("storage_considerations", "").strip()
        pr.value_addition_notes = request.form.get("value_addition_notes", "").strip()

        db.session.commit()
        log_admin_activity("Updated product entry", "CropProduct", pr.id)
        flash(f"Product '{pr.product_name}' updated.", "success")
        return redirect(url_for("admin.products_list"))

    return render_template("admin/product_form.html", crops=crops, product=pr, title=f"Edit Product: {pr.product_name}")


@admin_bp.route("/products/<int:id>/delete", methods=["GET", "POST"])
@admin_required
def product_delete(id):
    pr = db.get_or_404(CropProduct, id)
    if request.method == "POST":
        name = pr.product_name
        db.session.delete(pr)
        db.session.commit()
        log_admin_activity("Deleted product entry", "CropProduct", id)
        flash(f"Product '{name}' deleted.", "info")
        return redirect(url_for("admin.products_list"))

    return render_template(
        "admin/confirm_delete.html",
        title="Confirm Delete Product",
        item_name=pr.product_name,
        back_url=url_for("admin.products_list"),
    )
