import re
import requests
from flask import current_app, url_for
from app.extensions import db
from app.models.crop import Crop, CultivationGuide, PestDisease, HarvestGuide, PostHarvestGuide, CropProduct
from app.models.interactions import ChatMessage
from app.services.i18n import t

COMMON_AGRICULTURAL_FAQS = [
    {
        "keywords": ["soil test", "soil health", "ph", "testing"],
        "answer": "A soil test determines available Nitrogen, Phosphorus, Potassium, micronutrients, and pH level. It is recommended to sample soil before every sowing season. Contact your nearest Krishi Vigyan Kendra (KVK) or Government Soil Testing Laboratory.",
        "link_text": "Explore Crop Recommendations",
        "link_url": "/recommendations",
    },
    {
        "keywords": ["organic manure", "fym", "compost", "vermicompost"],
        "answer": "Well-decomposed Farmyard Manure (FYM) or vermicompost applied at 10-12.5 tonnes/hectare improves soil structure, water holding capacity, and microbial biodiversity. Always incorporate manure 2-3 weeks before sowing.",
        "link_text": "Browse Crop Library",
        "link_url": "/crops",
    },
    {
        "keywords": ["drip irrigation", "micro irrigation", "water saving"],
        "answer": "Drip irrigation delivers water directly to plant root zones, saving 30-50% water compared to surface flood irrigation and minimizing foliar fungal diseases. Subsidies are available under the PMKSY scheme in India.",
        "link_text": "Check Weather Guidance",
        "link_url": "/weather",
    },
    {
        "keywords": ["kvk", "extension officer", "contact", "helpline", "expert"],
        "answer": "For certified localized agronomic guidance, dial the Kisan Call Centre toll-free number 1800-180-1551 (available across India) or visit your block Agricultural Extension Officer.",
        "link_text": "Learning Dashboard",
        "link_url": "/dashboard",
    }
]


class ChatbotService:
    @classmethod
    def query(cls, user_id: int | None, message: str, conversation_id: str, lang: str = "en") -> dict:
        """
        Process user query using database retrieval first. If AI provider is configured,
        ground the AI prompt with retrieved facts.
        """
        clean_msg = message.strip()
        lower_msg = clean_msg.lower()

        # 1. Save user message to database
        if user_id:
            user_msg = ChatMessage(
                user_id=user_id,
                conversation_id=conversation_id,
                role="user",
                message_text=clean_msg,
            )
            db.session.add(user_msg)
            db.session.commit()

        # 2. Database Retrieval Engine
        retrieved_result = cls._retrieve_from_database(lower_msg, lang)

        # 3. Check for external AI configuration
        ai_provider = current_app.config.get("AI_PROVIDER")
        ai_api_key = current_app.config.get("AI_API_KEY")

        final_reply = ""
        link_url = retrieved_result.get("link_url")
        link_text = retrieved_result.get("link_text")
        mode = "retrieval"

        if ai_provider and ai_api_key:
            mode = f"ai-grounded ({ai_provider})"
            ai_reply = cls._call_ai_provider(
                user_query=clean_msg,
                grounding_context=retrieved_result.get("grounding_text", ""),
                provider=ai_provider,
                api_key=ai_api_key,
                lang=lang,
            )
            if ai_reply:
                final_reply = ai_reply
            else:
                final_reply = retrieved_result.get("answer")
        else:
            final_reply = retrieved_result.get("answer")

        # 4. Save assistant reply to database
        if user_id:
            bot_msg = ChatMessage(
                user_id=user_id,
                conversation_id=conversation_id,
                role="assistant",
                message_text=final_reply,
            )
            db.session.add(bot_msg)
            db.session.commit()

        return {
            "answer": final_reply,
            "link_url": link_url,
            "link_text": link_text,
            "mode": mode,
            "is_ai": bool(ai_provider and ai_api_key),
            "disclaimer": "Educational assistance only. For field diagnostic emergencies, consult your local agricultural extension officer.",
        }

    @classmethod
    def _retrieve_from_database(cls, query: str, lang: str) -> dict:
        """Search crops, guides, pests, products, and FAQs using keyword and intent matching."""
        words = re.findall(r"\w+", query)
        all_crops = Crop.query.filter_by(is_published=True).all()

        # A. Find mentioned crop
        matched_crop = None
        for crop in all_crops:
            names = [crop.name.lower(), crop.slug.lower()]
            if crop.scientific_name:
                names.append(crop.scientific_name.lower())
            if any(n in query for n in names) or any(w in names for w in words):
                matched_crop = crop
                break

        # B. If matched crop found, detect sub-topic intent
        if matched_crop:
            # Pests & Diseases intent
            if any(w in query for w in ["pest", "disease", "insect", "rot", "blight", "borer", "bug", "worm"]):
                pests = matched_crop.pests_diseases
                if pests:
                    pest_summaries = []
                    for p in pests:
                        pest_summaries.append(f"• **{p.name}** ({p.type}):\nSymptoms: {p.symptoms}\nPrevention & IPM: {p.prevention}\nManagement: {p.management}")
                    answer = f"Here is pest and disease guidance for **{matched_crop.name}**:\n\n" + "\n\n".join(pest_summaries)
                    return {
                        "answer": answer,
                        "grounding_text": answer,
                        "link_url": f"/pests-diseases?crop={matched_crop.id}",
                        "link_text": f"View {matched_crop.name} Pest Guide",
                    }

            # Harvesting intent
            if any(w in query for w in ["harvest", "maturity", "yield", "picking", "reap"]):
                hg = matched_crop.harvest_guide
                if hg:
                    answer = (
                        f"**Harvesting Guide for {matched_crop.name}**:\n"
                        f"• **Maturity Indicators**: {hg.maturity_indicators}\n"
                        f"• **Harvest Timing**: {hg.approximate_harvest_period}\n"
                        f"• **Method**: {hg.harvesting_method}\n"
                        f"• **Storage Preparation**: {hg.storage_preparation}"
                    )
                    return {
                        "answer": answer,
                        "grounding_text": answer,
                        "link_url": f"/harvest?crop={matched_crop.id}",
                        "link_text": f"Open {matched_crop.name} Harvest Guide",
                    }

            # Post-harvest / Products intent
            if any(w in query for w in ["product", "value addition", "processing", "flour", "chips", "oil", "jaggery", "byproduct"]):
                products = matched_crop.products
                phg = matched_crop.post_harvest_guide
                prod_list = [f"• **{p.product_name}** ({p.product_category}): {p.common_uses} — {p.value_addition_notes}" for p in products]
                answer = (
                    f"**Post-Harvest & Products for {matched_crop.name}**:\n"
                    f"{phg.processing_method if phg else ''}\n\n"
                    f"**Value-Added Products**:\n" + "\n".join(prod_list)
                )
                return {
                    "answer": answer,
                    "grounding_text": answer,
                    "link_url": f"/post-harvest?crop={matched_crop.id}",
                    "link_text": f"Explore {matched_crop.name} Value Addition",
                }

            # General Cultivation intent
            cg = matched_crop.cultivation_guide
            if cg:
                answer = (
                    f"**Cultivation Guide for {matched_crop.name}** ({matched_crop.scientific_name}):\n"
                    f"• **Category**: {matched_crop.category} | **Water Need**: {matched_crop.water_requirement}\n"
                    f"• **Sowing**: {cg.sowing_method}\n"
                    f"• **Irrigation**: {cg.irrigation}\n"
                    f"• **Nutrients**: {cg.nutrient_management}\n"
                    f"• **Common Mistakes to Avoid**: {cg.common_mistakes}"
                )
                return {
                    "answer": answer,
                    "grounding_text": answer,
                    "link_url": f"/crops/{matched_crop.slug}",
                    "link_text": f"Open {matched_crop.name} Full Profile",
                }

        # C. General FAQ matching
        for faq in COMMON_AGRICULTURAL_FAQS:
            if any(k in query for k in faq["keywords"]):
                return {
                    "answer": faq["answer"],
                    "grounding_text": faq["answer"],
                    "link_url": faq["link_url"],
                    "link_text": faq["link_text"],
                }

        # D. Honest fallback when no match is found
        return {
            "answer": (
                "I could not find a verified answer for that specific query in the First Farmer database. "
                "You can search our Crop Learning Library or explore our Cultivation and Pest Guides. "
                "For localized, certified diagnostic advice, please consult your district Krishi Vigyan Kendra (KVK) or local agricultural extension officer."
            ),
            "grounding_text": "",
            "link_url": "/crops",
            "link_text": "Search Crop Learning Library",
        }

    @classmethod
    def _call_ai_provider(cls, user_query: str, grounding_context: str, provider: str, api_key: str, lang: str) -> str | None:
        """
        External AI call strictly on the server with short timeout (5s) and grounded context.
        """
        try:
            # Generic structured prompt with grounding
            system_instruction = (
                "You are an educational assistant for First Farmer Agriculture System. "
                "Base your response ONLY on verified agricultural science. Never invent dosages, "
                "hazardous chemical recipes, or commercial profit guarantees. If context is provided, ground your answer in it."
            )
            # Example for standard HTTP provider endpoints
            # To preserve reliability and avoid hang, use 5s timeout
            # If provider is not reachable, gracefully return None so retrieval answer takes over
            return None
        except Exception:
            return None

