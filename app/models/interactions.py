from datetime import datetime, timezone
from app.extensions import db

def utc_now():
    return datetime.now(timezone.utc)

class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    conversation_id = db.Column(db.String(64), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False)  # 'user', 'assistant'
    message_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    user = db.relationship("User", back_populates="chat_messages")


class Translation(db.Model):
    __tablename__ = "translations"
    __table_args__ = (
        db.UniqueConstraint("entity_type", "entity_id", "field_name", "language_code", name="uq_translation_entity_field"),
        db.Index("idx_translation_lookup", "entity_type", "entity_id", "language_code"),
    )

    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(60), nullable=False)  # 'crop', 'guide', 'product', 'ui'
    entity_id = db.Column(db.Integer, nullable=False)
    field_name = db.Column(db.String(60), nullable=False)
    language_code = db.Column(db.String(10), nullable=False)  # 'ta', 'hi'
    translated_title = db.Column(db.String(255), nullable=True)
    translated_content = db.Column(db.Text, nullable=False)

