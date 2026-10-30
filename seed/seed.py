import argparse
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db, hash_password
from app.models import (
    User,
    SoilType,
    Season,
    Region,
    Crop,
    CultivationGuide,
    PestDisease,
    HarvestGuide,
    PostHarvestGuide,
    CropProduct,
    LearningModule,
    QuizQuestion,
    Translation,
)
from seed.data import LOOKUP_DATA, CROPS_DATA, TRANSLATION_RECORDS

def seed_database(content_only: bool = False, with_demo_users: bool = False):
    app = create_app()
    with app.app_context():
        print(f"[*] Starting database seed (Environment: {app.config.get('APP_ENV')})...")
        db.create_all()

        # 1. Lookups: Soils
        soil_objs = {}
        for s in LOOKUP_DATA["soils"]:
            obj = SoilType.query.filter_by(name=s["name"]).first()
            if not obj:
                obj = SoilType(name=s["name"], description=s["description"])
                db.session.add(obj)
            soil_objs[s["name"]] = obj

        # Lookups: Seasons
        season_objs = {}
        for s in LOOKUP_DATA["seasons"]:
            obj = Season.query.filter_by(name=s["name"]).first()
            if not obj:
                obj = Season(name=s["name"], period=s["period"], description=s["description"])
                db.session.add(obj)
            season_objs[s["name"]] = obj

        # Lookups: Regions
        region_objs = {}
        for r in LOOKUP_DATA["regions"]:
            obj = Region.query.filter_by(name=r["name"]).first()
            if not obj:
                obj = Region(name=r["name"], state=r["state"], zone=r["zone"])
                db.session.add(obj)
            region_objs[r["name"]] = obj

        db.session.commit()
        print(f"[*] Seeded {len(soil_objs)} soils, {len(season_objs)} seasons, {len(region_objs)} regions.")

        # 2. Crops & Related Guides
        crop_id_map = {}
        for idx, c in enumerate(CROPS_DATA, 1):
            crop = Crop.query.filter_by(slug=c["slug"]).first()
            if not crop:
                crop = Crop(slug=c["slug"])
                db.session.add(crop)

            crop.name = c["name"]
            crop.scientific_name = c["scientific_name"]
            crop.category = c["category"]
            crop.description = c["description"]
            crop.water_requirement = c["water_requirement"]
            crop.season_summary = c["season_summary"]
            crop.soil_climate_summary = c["soil_climate_summary"]
            crop.image_path = c["image_path"]
            crop.min_temp = c["min_temp"]
            crop.max_temp = c["max_temp"]
            crop.min_rainfall = c["min_rainfall"]
            crop.max_rainfall = c["max_rainfall"]
            crop.climate_source_note = c["climate_source_note"]
            crop.difficulty_level = c["difficulty_level"]
            crop.is_published = True

            # Junctions
            crop.soils = [soil_objs[s] for s in c["soils"] if s in soil_objs]
            crop.seasons = [season_objs[s] for s in c["seasons"] if s in season_objs]
            crop.regions = [region_objs[r] for r in c["regions"] if r in region_objs]

            db.session.flush()
            crop_id_map[c["slug"]] = crop.id

            # Cultivation Guide
            cg = c["cultivation_guide"]
            guide = CultivationGuide.query.filter_by(crop_id=crop.id).first()
            if not guide:
                guide = CultivationGuide(crop_id=crop.id)
                db.session.add(guide)
            guide.seed_selection = cg["seed_selection"]
            guide.land_preparation = cg["land_preparation"]
            guide.sowing_method = cg["sowing_method"]
            guide.irrigation = cg["irrigation"]
            guide.nutrient_management = cg["nutrient_management"]
            guide.weed_management = cg["weed_management"]
            guide.growth_stages = cg["growth_stages"]
            guide.common_mistakes = cg["common_mistakes"]
            guide.source_reference = cg["source_reference"]
            guide.last_reviewed_at = cg["last_reviewed_at"]

            # Harvest Guide
            hg = c["harvest_guide"]
            hguide = HarvestGuide.query.filter_by(crop_id=crop.id).first()
            if not hguide:
                hguide = HarvestGuide(crop_id=crop.id)
                db.session.add(hguide)
            hguide.maturity_indicators = hg["maturity_indicators"]
            hguide.approximate_harvest_period = hg["approximate_harvest_period"]
            hguide.harvesting_method = hg["harvesting_method"]
            hguide.handling_precautions = hg["handling_precautions"]
            hguide.storage_preparation = hg["storage_preparation"]
            hguide.source_reference = hg["source_reference"]
            hguide.last_reviewed_at = hg["last_reviewed_at"]

            # Post-Harvest Guide
            phg = c["post_harvest_guide"]
            phguide = PostHarvestGuide.query.filter_by(crop_id=crop.id).first()
            if not phguide:
                phguide = PostHarvestGuide(crop_id=crop.id)
                db.session.add(phguide)
            phguide.cleaning_and_grading = phg["cleaning_and_grading"]
            phguide.storage_method = phg["storage_method"]
            phguide.preservation_method = phg["preservation_method"]
            phguide.processing_method = phg["processing_method"]
            phguide.packaging_method = phg["packaging_method"]
            phguide.food_uses = phg["food_uses"]
            phguide.industrial_uses = phg["industrial_uses"]
            phguide.by_products = phg["by_products"]
            phguide.source_reference = phg["source_reference"]
            phguide.last_reviewed_at = phg["last_reviewed_at"]

            # Pests & Diseases
            for pd in c["pests_diseases"]:
                existing_pd = PestDisease.query.filter_by(crop_id=crop.id, name=pd["name"]).first()
                if not existing_pd:
                    existing_pd = PestDisease(crop_id=crop.id, name=pd["name"])
                    db.session.add(existing_pd)
                existing_pd.type = pd["type"]
                existing_pd.symptoms = pd["symptoms"]
                existing_pd.contributing_conditions = pd["contributing_conditions"]
                existing_pd.prevention = pd["prevention"]
                existing_pd.management = pd["management"]
                existing_pd.source_reference = pd["source_reference"]
                existing_pd.last_reviewed_at = pd["last_reviewed_at"]

            # Products
            for pr in c["products"]:
                existing_pr = CropProduct.query.filter_by(crop_id=crop.id, product_name=pr["product_name"]).first()
                if not existing_pr:
                    existing_pr = CropProduct(crop_id=crop.id, product_name=pr["product_name"])
                    db.session.add(existing_pr)
                existing_pr.product_category = pr["product_category"]
                existing_pr.raw_material = pr["raw_material"]
                existing_pr.processing_overview = pr["processing_overview"]
                existing_pr.common_uses = pr["common_uses"]
                existing_pr.storage_considerations = pr["storage_considerations"]
                existing_pr.value_addition_notes = pr["value_addition_notes"]

            # Learning Module
            lm_slug = f"module-{c['slug']}"
            lm = LearningModule.query.filter_by(slug=lm_slug).first()
            if not lm:
                lm = LearningModule(slug=lm_slug)
                db.session.add(lm)
            lm.crop_id = crop.id
            lm.title = f"Mastering {c['name']} Production & Value Addition"
            lm.content_summary = f"Comprehensive curriculum covering cultivation, pest protection, harvesting, and commercial value-addition for {c['name']}."
            lm.sort_order = idx

            # Quizzes
            for q in c["quiz"]:
                existing_q = QuizQuestion.query.filter_by(crop_id=crop.id, question_text=q["question"]).first()
                if not existing_q:
                    existing_q = QuizQuestion(crop_id=crop.id, question_text=q["question"])
                    db.session.add(existing_q)
                existing_q.option_a = q["option_a"]
                existing_q.option_b = q["option_b"]
                existing_q.option_c = q["option_c"]
                existing_q.option_d = q["option_d"]
                existing_q.correct_option = q["correct_option"]
                existing_q.explanation = q["explanation"]

        db.session.commit()
        print(f"[*] Seeded {len(CROPS_DATA)} crops with complete cultivation, pest, harvest, post-harvest, product, and quiz records.")

        # 3. Translations
        for tr in TRANSLATION_RECORDS:
            crop_id = crop_id_map.get(tr["slug"])
            if not crop_id:
                continue
            rec = Translation.query.filter_by(
                entity_type=tr["entity_type"],
                entity_id=crop_id,
                field_name=tr["field"],
                language_code=tr["lang"]
            ).first()
            if not rec:
                rec = Translation(
                    entity_type=tr["entity_type"],
                    entity_id=crop_id,
                    field_name=tr["field"],
                    language_code=tr["lang"],
                )
                db.session.add(rec)
            rec.translated_title = tr["title"]
            rec.translated_content = tr["content"]

        db.session.commit()
        print(f"[*] Seeded {len(TRANSLATION_RECORDS)} multilingual database translation records.")

        # 4. Demo Users (optional, rejected in production)
        if with_demo_users:
            env = app.config.get("APP_ENV", "development")
            if env == "production":
                print("[!] ERROR: Refusing to create demo accounts in production (APP_ENV=production).")
                sys.exit(1)

            # Demo Student
            student = User.query.filter_by(email="student@firstfarmer.org").first()
            if not student:
                student = User(
                    full_name="Priya Sharma (Student)",
                    email="student@firstfarmer.org",
                    password_hash=hash_password("StudentPass123!"),
                    role="student",
                    preferred_language="en",
                )
                db.session.add(student)

            # Demo Admin
            admin = User.query.filter_by(email="admin@firstfarmer.org").first()
            if not admin:
                admin = User(
                    full_name="System Administrator",
                    email="admin@firstfarmer.org",
                    password_hash=hash_password("AdminPass123!"),
                    role="admin",
                    preferred_language="en",
                )
                db.session.add(admin)

            db.session.commit()
            print("[*] Seeded development demo accounts:")
            print("    - Student: student@firstfarmer.org / StudentPass123!")
            print("    - Admin:   admin@firstfarmer.org / AdminPass123!")
            print("    [!] IMPORTANT: Change demo passwords before deploying or sharing.")

        print("[OK] Database seeding completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="First Farmer Database Seeder")
    parser.add_argument("--content-only", action="store_true", help="Seed only agricultural crops, guides, and translations (no demo users)")
    parser.add_argument("--with-demo-users", action="store_true", help="Seed development demo student and admin users")
    args = parser.parse_args()

    # Default to with-demo-users in development if neither is specified
    with_users = args.with_demo_users or (not args.content_only)
    seed_database(content_only=args.content_only, with_demo_users=with_users)
