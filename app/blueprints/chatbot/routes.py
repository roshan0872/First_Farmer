import uuid
from flask import Blueprint, render_template, session, g
from app.models.interactions import ChatMessage
from app.services.security import login_required

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/chatbot")
def index():
    """Page 11 — Agriculture Learning Chatbot."""
    # Ensure a conversation_id is present in session
    if "conv_id" not in session:
        session["conv_id"] = str(uuid.uuid4())

    history = []
    if g.current_user:
        history = (
            ChatMessage.query.filter_by(user_id=g.current_user.id)
            .order_by(ChatMessage.created_at.asc())
            .limit(50)
            .all()
        )

    suggested_questions = [
        "How to manage tomato fruit borer effectively?",
        "What is Alternate Wetting and Drying (AWD) in rice?",
        "When is sugarcane ready for harvest?",
        "Why is gypsum applied to groundnut at pegging stage?",
        "What are the best value-added products made from green bananas?",
        "How can I test my soil health before sowing?",
    ]

    return render_template(
        "chatbot/index.html",
        history=history,
        suggested_questions=suggested_questions,
        conversation_id=session["conv_id"],
    )

