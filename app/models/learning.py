from datetime import datetime, timezone
from app.extensions import db

def utc_now():
    return datetime.now(timezone.utc)

class CropBookmark(db.Model):
    __tablename__ = "crop_bookmarks"
    __table_args__ = (db.UniqueConstraint("user_id", "crop_id", name="uq_user_crop_bookmark"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    user = db.relationship("User", back_populates="bookmarks")
    crop = db.relationship("Crop", back_populates="bookmarks")


class CropView(db.Model):
    __tablename__ = "crop_views"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True)
    viewed_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    user = db.relationship("User", back_populates="crop_views")
    crop = db.relationship("Crop")


class LearningModule(db.Model):
    __tablename__ = "learning_modules"

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), nullable=True, index=True)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    content_summary = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)

    crop = db.relationship("Crop", back_populates="learning_module")
    progress_records = db.relationship("LearningProgress", back_populates="module", cascade="all, delete-orphan")


class LearningProgress(db.Model):
    __tablename__ = "learning_progress"
    __table_args__ = (db.UniqueConstraint("user_id", "learning_module_id", name="uq_user_module_progress"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    learning_module_id = db.Column(db.Integer, db.ForeignKey("learning_modules.id", ondelete="CASCADE"), nullable=False, index=True)
    completion_status = db.Column(db.String(30), default="in_progress", nullable=False)  # 'not_started', 'in_progress', 'completed'
    progress_percentage = db.Column(db.Integer, default=0, nullable=False)
    last_accessed_at = db.Column(db.DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    user = db.relationship("User", back_populates="learning_progress")
    module = db.relationship("LearningModule", back_populates="progress_records")


class QuizQuestion(db.Model):
    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(2), nullable=False)  # 'A', 'B', 'C', 'D'
    explanation = db.Column(db.Text, nullable=True)

    crop = db.relationship("Crop", back_populates="quiz_questions")


class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    user = db.relationship("User", back_populates="quiz_attempts")
    crop = db.relationship("Crop")
