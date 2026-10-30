from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.extensions import db, hash_password, verify_password
from app.models.user import User
from app.forms import RegistrationForm, LoginForm
from app.services.security import is_login_locked, record_login_failure, clear_login_attempts
from app.services.i18n import t

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Page 2 — Student / Learner Registration."""
    if g.current_user:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        email_clean = form.email.data.strip().lower()
        existing = User.query.filter_by(email=email_clean).first()
        if existing:
            form.email.errors.append("An account with this email address is already registered.")
            return render_template("auth/register.html", form=form)

        user = User(
            full_name=form.full_name.data.strip(),
            email=email_clean,
            password_hash=hash_password(form.password.data),
            role="student",
            preferred_language=form.preferred_language.data,
        )
        db.session.add(user)
        db.session.commit()

        # Set session on registration
        session.clear()
        session["user_id"] = user.id
        session["lang"] = user.preferred_language
        flash("Welcome to First Farmer! Your learning account has been created successfully.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Page 2 — User Login with Database-Backed Throttling."""
    if g.current_user:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    next_url = request.args.get("next")

    if form.validate_on_submit():
        email_clean = form.email.data.strip().lower()

        # Check database-backed lockout
        if is_login_locked(email_clean):
            flash(t("auth_throttled"), "error")
            return render_template("auth/login.html", form=form)

        user = User.query.filter_by(email=email_clean).first()
        if not user or not verify_password(user.password_hash, form.password.data):
            record_login_failure(email_clean)
            flash(t("auth_invalid_credentials"), "error")
            return render_template("auth/login.html", form=form)

        # Successful login: reset attempts and establish new session
        clear_login_attempts(email_clean)
        session.clear()
        session["user_id"] = user.id
        session["lang"] = user.preferred_language

        flash(f"Welcome back, {user.full_name}!", "success")
        if next_url and next_url.startswith("/"):
            return redirect(next_url)
        return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
def logout():
    """Logout action with session reset."""
    session.clear()
    flash("You have been logged out securely.", "info")
    return redirect(url_for("main.index"))

