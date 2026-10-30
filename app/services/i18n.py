import json
import os
from flask import session, request, g
from app.models.interactions import Translation

_I18N_DATA = {}

def load_translations(app_root: str):
    """Load JSON translation dictionaries into memory."""
    global _I18N_DATA
    i18n_dir = os.path.join(app_root, "i18n")
    for lang in ["en", "ta", "hi"]:
        file_path = os.path.join(i18n_dir, f"{lang}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    _I18N_DATA[lang] = json.load(f)
                except Exception:
                    _I18N_DATA[lang] = {}
        else:
            _I18N_DATA[lang] = {}


def get_current_language() -> str:
    """Determine the active language code."""
    # 1. Active session
    lang = session.get("lang")
    if lang in ["en", "ta", "hi"]:
        return lang
    
    # 2. Authenticated user preference
    if hasattr(g, "current_user") and g.current_user and g.current_user.preferred_language:
        if g.current_user.preferred_language in ["en", "ta", "hi"]:
            session["lang"] = g.current_user.preferred_language
            return g.current_user.preferred_language

    # 3. Cookie
    lang_cookie = request.cookies.get("pref_lang")
    if lang_cookie in ["en", "ta", "hi"]:
        return lang_cookie

    return "en"


def t(key: str, lang: str | None = None, default: str | None = None) -> str:
    """Translate a UI key with fallback to English then default."""
    if not lang:
        lang = get_current_language()

    # Direct key lookup in target language
    val = _I18N_DATA.get(lang, {}).get(key)
    if val:
        return val

    # Fallback to English
    val_en = _I18N_DATA.get("en", {}).get(key)
    if val_en:
        return val_en

    return default if default is not None else key


def get_entity_translation(entity_type: str, entity_id: int, field_name: str, lang: str | None = None) -> tuple[str | None, bool]:
    """
    Retrieve translated title or content for an entity from database.
    Returns (translated_text, is_translated). If not translated, returns (None, False).
    """
    if not lang:
        lang = get_current_language()

    if lang == "en":
        return None, True  # Default language is always native

    tr = Translation.query.filter_by(
        entity_type=entity_type,
        entity_id=entity_id,
        field_name=field_name,
        language_code=lang,
    ).first()

    if tr and tr.translated_content:
        return tr.translated_content, True

    return None, False

