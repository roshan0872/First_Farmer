from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from app.extensions import db
from app.models.crop import Crop
from app.models.learning import (
    CropBookmark,
    CropView,
    LearningModule,
    LearningProgress,
    QuizQuestion,
    QuizAttempt,
)
from app.services.security import login_required

learning_bp = Blueprint("learning", __name__)

@learning_bp.route("/learning")
@login_required
def progress():
    """Page 12 — My Learning Progress & Dashboard."""
    user = g.current_user

    # 1. Saved Crops
    bookmarks = (
        CropBookmark.query.filter_by(user_id=user.id)
        .order_by(CropBookmark.created_at.desc())
        .all()
    )
    saved_crops = [b.crop for b in bookmarks]

    # 2. Recently Viewed Crops
    views = (
        CropView.query.filter_by(user_id=user.id)
        .order_by(CropView.viewed_at.desc())
        .limit(6)
        .all()
    )
    viewed_crops = [v.crop for v in views]

    # 3. Completed & In-Progress Modules
    all_modules = LearningModule.query.order_by(LearningModule.sort_order.asc()).all()
    total_modules_count = len(all_modules)

    progress_records = LearningProgress.query.filter_by(user_id=user.id).all()
    completed_module_ids = {
        p.learning_module_id for p in progress_records if p.completion_status == "completed"
    }

    completion_percentage = 0
    if total_modules_count > 0:
        completion_percentage = int(round((len(completed_module_ids) / total_modules_count) * 100))

    # 4. Quiz Attempts
    quiz_attempts = (
        QuizAttempt.query.filter_by(user_id=user.id)
        .order_by(QuizAttempt.completed_at.desc())
        .limit(10)
        .all()
    )

    # 5. Recommended Next Topics (modules not yet completed)
    recommended_modules = [m for m in all_modules if m.id not in completed_module_ids][:3]

    return render_template(
        "learning/progress.html",
        saved_crops=saved_crops,
        viewed_crops=viewed_crops,
        all_modules=all_modules,
        completed_module_ids=completed_module_ids,
        completion_percentage=completion_percentage,
        quiz_attempts=quiz_attempts,
        recommended_modules=recommended_modules,
    )


@learning_bp.route("/learning/module/<slug>/complete", methods=["POST"])
@login_required
def toggle_module_complete(slug):
    """Mark a module as completed or toggle back."""
    user = g.current_user
    module = LearningModule.query.filter_by(slug=slug).first_or_404()

    progress = LearningProgress.query.filter_by(user_id=user.id, learning_module_id=module.id).first()
    if not progress:
        progress = LearningProgress(
            user_id=user.id,
            learning_module_id=module.id,
            completion_status="completed",
            progress_percentage=100,
        )
        db.session.add(progress)
        flash(f"Congratulations! You completed the learning module: '{module.title}'.", "success")
    else:
        if progress.completion_status == "completed":
            progress.completion_status = "in_progress"
            progress.progress_percentage = 50
            flash(f"Module '{module.title}' status changed to in-progress.", "info")
        else:
            progress.completion_status = "completed"
            progress.progress_percentage = 100
            flash(f"Module '{module.title}' marked as completed!", "success")

    progress.last_accessed_at = datetime.now(timezone.utc)
    db.session.commit()

    return redirect(request.referrer or url_for("crops.detail", slug=module.crop.slug if module.crop else "rice-paddy"))


@learning_bp.route("/learning/bookmark/<int:crop_id>", methods=["POST"])
@login_required
def toggle_bookmark(crop_id):
    """Toggle bookmark on a crop (supports AJAX fetch and standard form post)."""
    user = g.current_user
    crop = db.get_or_404(Crop, crop_id)

    existing = CropBookmark.query.filter_by(user_id=user.id, crop_id=crop.id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        bookmarked = False
        msg = f"Removed {crop.name} from your saved crops."
    else:
        new_bm = CropBookmark(user_id=user.id, crop_id=crop.id)
        db.session.add(new_bm)
        db.session.commit()
        bookmarked = True
        msg = f"Saved {crop.name} to your learning bookmarks."

    # Return JSON for JavaScript fetch requests
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        return jsonify({"success": True, "bookmarked": bookmarked, "message": msg})

    flash(msg, "info")
    return redirect(request.referrer or url_for("crops.detail", slug=crop.slug))


@learning_bp.route("/learning/quiz/<slug>", methods=["GET", "POST"])
@login_required
def quiz(slug):
    """Lightweight 3-question quiz for a crop with server-side validation and explanations."""
    crop = Crop.query.filter_by(slug=slug).first_or_404()
    questions = crop.quiz_questions

    if not questions:
        flash(f"No quiz questions available for {crop.name} yet.", "info")
        return redirect(url_for("crops.detail", slug=crop.slug))

    results = None
    if request.method == "POST":
        score = 0
        total = len(questions)
        user_answers = {}
        graded_questions = []

        for q in questions:
            user_opt = request.form.get(f"question_{q.id}", "").strip().upper()
            user_answers[q.id] = user_opt
            is_correct = (user_opt == q.correct_option)
            if is_correct:
                score += 1

            graded_questions.append({
                "question": q,
                "user_answer": user_opt,
                "is_correct": is_correct,
                "correct_option": q.correct_option,
                "explanation": q.explanation,
            })

        # Save quiz attempt
        attempt = QuizAttempt(
            user_id=g.current_user.id,
            crop_id=crop.id,
            score=score,
            total_questions=total,
        )
        db.session.add(attempt)
        db.session.commit()

        results = {
            "score": score,
            "total": total,
            "percentage": int(round((score / total) * 100)),
            "graded_questions": graded_questions,
        }

    return render_template(
        "learning/quiz.html",
        crop=crop,
        questions=questions,
        results=results,
    )
