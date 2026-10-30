from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session
from app.extensions import db, verify_password, hash_password
from app.models.learning import CropBookmark
from app.models.interactions import ChatMessage
from app.forms import ProfileUpdateForm, ChangePasswordForm
from app.services.security import login_required

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def index():
    """Page 13 — Profile and Settings."""
    user = g.current_user
    profile_form = ProfileUpdateForm(obj=user)
    password_form = ChangePasswordForm()

    if profile_form.validate_on_submit() and "submit_profile" in request.form:
        user.full_name = profile_form.full_name.data.strip()
        user.preferred_language = profile_form.preferred_language.data
        session["lang"] = user.preferred_language
        db.session.commit()
        flash("Profile information updated successfully.", "success")
        return redirect(url_for("profile.index"))

    bookmarks = CropBookmark.query.filter_by(user_id=user.id).all()
    chat_count = ChatMessage.query.filter_by(user_id=user.id).count()

    return render_template(
        "profile/index.html",
        user=user,
        profile_form=profile_form,
        password_form=password_form,
        bookmarks=bookmarks,
        chat_count=chat_count,
    )


@profile_bp.route("/profile/change-password", methods=["POST"])
@login_required
def change_password():
    """Secure password change enforcing verification and Argon2id re-hashing."""
    user = g.current_user
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not verify_password(user.password_hash, form.current_password.data):
            flash("Current password is incorrect.", "error")
            return redirect(url_for("profile.index"))

        user.password_hash = hash_password(form.new_password.data)
        db.session.commit()
        flash("Your password has been changed successfully.", "success")
        return redirect(url_for("profile.index"))

    for field, errors in form.errors.items():
        for err in errors:
            flash(f"Password error: {err}", "error")
    return redirect(url_for("profile.index"))


@profile_bp.route("/profile/clear-chat", methods=["POST"])
@login_required
def clear_chat():
    """Privacy action to clear user's stored chatbot history."""
    user = g.current_user
    ChatMessage.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    flash("Your agriculture chatbot conversation history has been cleared.", "info")
    return redirect(request.referrer or url_for("profile.index"))

