from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, g
from app.extensions import db
from app.models.crop import Crop, CropProduct
from app.models.learning import LearningProgress, CropBookmark, QuizAttempt
from app.services.i18n import get_current_language, t

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    """Page 1 — Welcome / Landing Page."""
    featured_crops = Crop.query.filter_by(is_published=True).limit(6).all()
    total_crops_count = Crop.query.filter_by(is_published=True).count()
    return render_template(
        "main/index.html",
        featured_crops=featured_crops,
        total_crops_count=total_crops_count,
    )


@main_bp.route("/dashboard")
def dashboard():
    """Page 3 — User Dashboard."""
    total_crops = Crop.query.filter_by(is_published=True).count()
    featured_products = CropProduct.query.limit(4).all()

    # User-specific metrics if logged in
    saved_crops_count = 0
    completed_modules_count = 0
    recent_quiz_results = []
    recently_viewed = []
    crops_by_category = {}

    # Category distribution for Chart.js
    categories = db.session.query(Crop.category, db.func.count(Crop.id)).filter_by(is_published=True).group_by(Crop.category).all()
    category_labels = [c[0] for c in categories]
    category_counts = [c[1] for c in categories]

    if g.current_user:
        saved_crops_count = CropBookmark.query.filter_by(user_id=g.current_user.id).count()
        completed_modules_count = LearningProgress.query.filter_by(
            user_id=g.current_user.id, completion_status="completed"
        ).count()
        recent_quiz_results = (
            QuizAttempt.query.filter_by(user_id=g.current_user.id)
            .order_by(QuizAttempt.completed_at.desc())
            .limit(5)
            .all()
        )
        recently_viewed = (
            Crop.query.join(Crop.bookmarks)
            .filter(CropBookmark.user_id == g.current_user.id)
            .limit(4)
            .all()
        )

    return render_template(
        "main/dashboard.html",
        total_crops=total_crops,
        featured_products=featured_products,
        saved_crops_count=saved_crops_count,
        completed_modules_count=completed_modules_count,
        recent_quiz_results=recent_quiz_results,
        recently_viewed=recently_viewed,
        category_labels=category_labels,
        category_counts=category_counts,
    )


@main_bp.route("/healthz")
def healthz():
    """Health check endpoint for Vercel/uptime probes."""
    try:
        # Check database connectivity
        db.session.execute(db.text("SELECT 1"))
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "app_env": main_bp.name,
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }), 500


@main_bp.route("/set-language/<lang>")
def set_language(lang):
    """Change active UI language and save to session/cookie/user preference."""
    if lang in ["en", "ta", "hi"]:
        session["lang"] = lang
        if g.current_user:
            g.current_user.preferred_language = lang
            db.session.commit()

    next_url = request.referrer or url_for("main.index")
    resp = redirect(next_url)
    resp.set_cookie("pref_lang", lang, max_age=86400 * 365, samesite="Lax")
    return resp
