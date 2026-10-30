from app.extensions import db

# Junction Tables
crop_soils = db.Table(
    "crop_soils",
    db.Column("crop_id", db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), primary_key=True),
    db.Column("soil_type_id", db.Integer, db.ForeignKey("soil_types.id", ondelete="CASCADE"), primary_key=True),
)

crop_seasons = db.Table(
    "crop_seasons",
    db.Column("crop_id", db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), primary_key=True),
    db.Column("season_id", db.Integer, db.ForeignKey("seasons.id", ondelete="CASCADE"), primary_key=True),
)

crop_regions = db.Table(
    "crop_regions",
    db.Column("crop_id", db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), primary_key=True),
    db.Column("region_id", db.Integer, db.ForeignKey("regions.id", ondelete="CASCADE"), primary_key=True),
)


class SoilType(db.Model):
    __tablename__ = "soil_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)

    crops = db.relationship("Crop", secondary=crop_soils, back_populates="soils")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class Season(db.Model):
    __tablename__ = "seasons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    period = db.Column(db.String(120), nullable=True)  # e.g., 'June to October'
    description = db.Column(db.String(255), nullable=True)

    crops = db.relationship("Crop", secondary=crop_seasons, back_populates="seasons")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "period": self.period, "description": self.description}


class Region(db.Model):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    state = db.Column(db.String(100), nullable=True)  # e.g., 'Tamil Nadu', 'Punjab'
    zone = db.Column(db.String(100), nullable=True)   # e.g., 'Southern Zone', 'Cauvery Delta'

    crops = db.relationship("Crop", secondary=crop_regions, back_populates="regions")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "state": self.state, "zone": self.zone}
