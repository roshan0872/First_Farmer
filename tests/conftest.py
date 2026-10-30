import pytest
from app import create_app
from app.extensions import db, hash_password
from app.models import User, SoilType, Season, Region, Crop
from seed.data import LOOKUP_DATA, CROPS_DATA

@pytest.fixture
def app():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

        # Seed minimal fixtures for tests
        soil = SoilType(name="Loamy", description="Balanced loam")
        season = Season(name="Kharif", period="Monsoon")
        region = Region(name="Tamil Nadu (Cauvery Delta)", state="Tamil Nadu")
        db.session.add_all([soil, season, region])

        crop = Crop(
            name="Rice (Paddy)",
            slug="rice-paddy",
            category="Cereal",
            description="Staple cereal crop.",
            water_requirement="High",
            season_summary="Kharif",
            difficulty_level="Beginner",
            is_published=True,
        )
        crop.soils.append(soil)
        crop.seasons.append(season)
        crop.regions.append(region)
        db.session.add(crop)

        # Seed standard student user
        student = User(
            full_name="Priya Student",
            email="student@firstfarmer.org",
            password_hash=hash_password("StudentPass123!"),
            role="student",
            preferred_language="en",
        )
        # Seed administrator user
        admin = User(
            full_name="Admin User",
            email="admin@firstfarmer.org",
            password_hash=hash_password("AdminPass123!"),
            role="admin",
            preferred_language="en",
        )
        db.session.add_all([student, admin])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def student_client(app, client):
    with client.session_transaction() as sess:
        student = User.query.filter_by(email="student@firstfarmer.org").first()
        sess["user_id"] = student.id
        sess["lang"] = "en"
    return client


@pytest.fixture
def admin_client(app, client):
    with client.session_transaction() as sess:
        admin = User.query.filter_by(email="admin@firstfarmer.org").first()
        sess["user_id"] = admin.id
        sess["lang"] = "en"
    return client
