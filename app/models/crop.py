from datetime import datetime, timezone
from app.extensions import db
from app.models.lookups import crop_soils, crop_seasons, crop_regions

def utc_now():
    return datetime.now(timezone.utc)

class Crop(db.Model):
    __tablename__ = "crops"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    scientific_name = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(60), nullable=False, index=True)  # 'Cereal', 'Pulse', 'Vegetable', 'Fruit', 'Cash Crop', 'Millets'
    description = db.Column(db.Text, nullable=False)
    water_requirement = db.Column(db.String(20), nullable=False)  # 'Low', 'Medium', 'High'
    season_summary = db.Column(db.String(200), nullable=True)
    soil_climate_summary = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    min_temp = db.Column(db.Float, nullable=True)  # °C
    max_temp = db.Column(db.Float, nullable=True)  # °C
    min_rainfall = db.Column(db.Float, nullable=True)  # mm
    max_rainfall = db.Column(db.Float, nullable=True)  # mm
    climate_source_note = db.Column(db.String(255), nullable=True)
    difficulty_level = db.Column(db.String(30), default="Beginner", nullable=False)  # 'Beginner', 'Intermediate', 'Advanced'
    is_published = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    # Junction Relationships
    soils = db.relationship("SoilType", secondary=crop_soils, back_populates="crops")
    seasons = db.relationship("Season", secondary=crop_seasons, back_populates="crops")
    regions = db.relationship("Region", secondary=crop_regions, back_populates="crops")

    # 1:1 and 1:N Relationships
    cultivation_guide = db.relationship("CultivationGuide", back_populates="crop", uselist=False, cascade="all, delete-orphan")
    harvest_guide = db.relationship("HarvestGuide", back_populates="crop", uselist=False, cascade="all, delete-orphan")
    post_harvest_guide = db.relationship("PostHarvestGuide", back_populates="crop", uselist=False, cascade="all, delete-orphan")
    pests_diseases = db.relationship("PestDisease", back_populates="crop", cascade="all, delete-orphan")
    products = db.relationship("CropProduct", back_populates="crop", cascade="all, delete-orphan")
    learning_module = db.relationship("LearningModule", back_populates="crop", uselist=False, cascade="all, delete-orphan")
    quiz_questions = db.relationship("QuizQuestion", back_populates="crop", cascade="all, delete-orphan")
    bookmarks = db.relationship("CropBookmark", back_populates="crop", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "scientific_name": self.scientific_name,
            "category": self.category,
            "description": self.description,
            "water_requirement": self.water_requirement,
            "season_summary": self.season_summary,
            "soil_climate_summary": self.soil_climate_summary,
            "image_path": self.image_path,
            "min_temp": self.min_temp,
            "max_temp": self.max_temp,
            "min_rainfall": self.min_rainfall,
            "max_rainfall": self.max_rainfall,
            "difficulty_level": self.difficulty_level,
            "is_published": self.is_published,
            "soils": [s.name for s in self.soils],
            "seasons": [s.name for s in self.seasons],
            "regions": [r.name for r in self.regions],
        }


class FarmProfile(db.Model):
    __tablename__ = "farm_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    region = db.Column(db.String(120), nullable=True)
    soil_type = db.Column(db.String(80), nullable=True)
    season = db.Column(db.String(80), nullable=True)
    water_availability = db.Column(db.String(30), nullable=True)  # 'Low', 'Medium', 'High'
    temperature = db.Column(db.Float, nullable=True)
    rainfall = db.Column(db.Float, nullable=True)
    source_information = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    user = db.relationship("User", back_populates="farm_profiles")


class CultivationGuide(db.Model):
    __tablename__ = "cultivation_guides"

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    seed_selection = db.Column(db.Text, nullable=False)
    land_preparation = db.Column(db.Text, nullable=False)
    sowing_method = db.Column(db.Text, nullable=False)
    irrigation = db.Column(db.Text, nullable=False)
    nutrient_management = db.Column(db.Text, nullable=False)
    weed_management = db.Column(db.Text, nullable=False)
    growth_stages = db.Column(db.Text, nullable=False)
    common_mistakes = db.Column(db.Text, nullable=False)
    source_reference = db.Column(db.String(255), nullable=True)
    last_reviewed_at = db.Column(db.String(50), nullable=True)

    crop = db.relationship("Crop", back_populates="cultivation_guide")


class PestDisease(db.Model):
    __tablename__ = "pests_diseases"

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    type = db.Column(db.String(40), nullable=False)  # 'pest', 'disease', 'other'
    symptoms = db.Column(db.Text, nullable=False)
    contributing_conditions = db.Column(db.Text, nullable=False)
    prevention = db.Column(db.Text, nullable=False)
    management = db.Column(db.Text, nullable=False)
    source_reference = db.Column(db.String(255), nullable=True)
    last_reviewed_at = db.Column(db.String(50), nullable=True)

    crop = db.relationship("Crop", back_populates="pests_diseases")


class HarvestGuide(db.Model):
    __tablename__ = "harvest_guides"

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    maturity_indicators = db.Column(db.Text, nullable=False)
    approximate_harvest_period = db.Column(db.String(120), nullable=False)
    harvesting_method = db.Column(db.Text, nullable=False)
    handling_precautions = db.Column(db.Text, nullable=False)
    storage_preparation = db.Column(db.Text, nullable=False)
    source_reference = db.Column(db.String(255), nullable=True)
    last_reviewed_at = db.Column(db.String(50), nullable=True)

    crop = db.relationship("Crop", back_populates="harvest_guide")


class PostHarvestGuide(db.Model):
    __tablename__ = "post_harvest_guides"

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    cleaning_and_grading = db.Column(db.Text, nullable=False)
    storage_method = db.Column(db.Text, nullable=False)
    preservation_method = db.Column(db.Text, nullable=False)
    processing_method = db.Column(db.Text, nullable=False)
    packaging_method = db.Column(db.Text, nullable=False)
    food_uses = db.Column(db.Text, nullable=False)
    industrial_uses = db.Column(db.Text, nullable=False)
    by_products = db.Column(db.Text, nullable=False)
    source_reference = db.Column(db.String(255), nullable=True)
    last_reviewed_at = db.Column(db.String(50), nullable=True)

    crop = db.relationship("Crop", back_populates="post_harvest_guide")


class CropProduct(db.Model):
    __tablename__ = "crop_products"

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True)
    product_name = db.Column(db.String(120), nullable=False, index=True)
    product_category = db.Column(db.String(60), nullable=False)  # 'Food Product', 'Industrial Product', 'By-Product'
    raw_material = db.Column(db.String(150), nullable=False)
    processing_overview = db.Column(db.Text, nullable=False)
    common_uses = db.Column(db.Text, nullable=False)
    storage_considerations = db.Column(db.Text, nullable=False)
    value_addition_notes = db.Column(db.Text, nullable=False)

    crop = db.relationship("Crop", back_populates="products")
