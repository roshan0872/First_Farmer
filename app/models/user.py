from datetime import datetime, timezone
from app.extensions import db

def utc_now():
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="student", nullable=False)  # 'student', 'admin'
    preferred_language = db.Column(db.String(10), default="en", nullable=False)  # 'en', 'ta', 'hi'
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    # Relationships
    bookmarks = db.relationship("CropBookmark", back_populates="user", cascade="all, delete-orphan")
    farm_profiles = db.relationship("FarmProfile", back_populates="user", cascade="all, delete-orphan")
    learning_progress = db.relationship("LearningProgress", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = db.relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    chat_messages = db.relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    crop_views = db.relationship("CropView", back_populates="user", cascade="all, delete-orphan")

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "preferred_language": self.preferred_language,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class LoginAttempt(db.Model):
    """Database-backed throttling for serverless authentication."""
    __tablename__ = "login_attempts"

    id = db.Column(db.Integer, primary_key=True)
    key_hash = db.Column(db.String(128), unique=True, nullable=False, index=True)  # hash of email/ip
    attempts_count = db.Column(db.Integer, default=1, nullable=False)
    last_attempt_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)
    locked_until = db.Column(db.DateTime(timezone=True), nullable=True)


class ActivityLog(db.Model):
    """Audit log for user and administrative actions."""
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = db.Column(db.String(80), nullable=False)
    entity_type = db.Column(db.String(80), nullable=False)
    entity_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)
