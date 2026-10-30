from functools import wraps
import hashlib
from datetime import datetime, timezone, timedelta
from flask import session, redirect, url_for, request, abort, jsonify, g
from app.extensions import db
from app.models.user import User, LoginAttempt

def get_current_user() -> User | None:
    """Retrieve current logged in user from session."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.current_user:
            if request.path.startswith("/api/"):
                return jsonify({"error": "Authentication required"}), 401
            return redirect(url_for("auth.login", next=request.full_path if request.method == "GET" else url_for("main.dashboard")))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.current_user:
            if request.path.startswith("/api/"):
                return jsonify({"error": "Authentication required"}), 401
            return redirect(url_for("auth.login", next=request.full_path if request.method == "GET" else url_for("admin.index")))
        if not g.current_user.is_admin:
            if request.path.startswith("/api/"):
                return jsonify({"error": "Forbidden: Administrator role required"}), 403
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def make_key_hash(identifier: str) -> str:
    """Hash an identifier (email + IP) to protect user privacy in failed login table."""
    client_ip = request.remote_addr or "127.0.0.1"
    raw = f"{identifier.strip().lower()}:{client_ip}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def to_utc(dt: datetime | None) -> datetime | None:
    """Ensure datetime is offset-aware UTC across SQLite and Postgres."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def is_login_locked(identifier: str) -> bool:
    """Check if login is locked due to repeated failures."""
    kh = make_key_hash(identifier)
    record = LoginAttempt.query.filter_by(key_hash=kh).first()
    if not record or not record.locked_until:
        return False
    now = datetime.now(timezone.utc)
    locked_until = to_utc(record.locked_until)
    if locked_until and locked_until > now:
        return True
    return False


def record_login_failure(identifier: str, max_attempts: int = 5, lock_minutes: int = 5):
    """Record failed login attempt and lock if threshold exceeded."""
    kh = make_key_hash(identifier)
    record = LoginAttempt.query.filter_by(key_hash=kh).first()
    now = datetime.now(timezone.utc)
    if not record:
        record = LoginAttempt(key_hash=kh, attempts_count=1, last_attempt_at=now)
        db.session.add(record)
    else:
        last_attempt = to_utc(record.last_attempt_at)
        # Reset counter if last attempt was older than lock window
        if last_attempt and last_attempt < now - timedelta(minutes=lock_minutes):
            record.attempts_count = 1
            record.locked_until = None
        else:
            record.attempts_count += 1
            if record.attempts_count >= max_attempts:
                record.locked_until = now + timedelta(minutes=lock_minutes)
        record.last_attempt_at = now
    db.session.commit()


def clear_login_attempts(identifier: str):
    """Clear failed login records after successful authentication."""
    kh = make_key_hash(identifier)
    LoginAttempt.query.filter_by(key_hash=kh).delete()
    db.session.commit()
