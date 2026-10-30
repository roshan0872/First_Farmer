from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    FloatField,
    TextAreaField,
    BooleanField,
    SubmitField,
    IntegerField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange, ValidationError

class RegistrationForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email Address", validators=[DataRequired(), Email(), Length(max=180)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters.")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    preferred_language = SelectField("Preferred Language", choices=[("en", "English"), ("ta", "Tamil (தமிழ்)"), ("hi", "Hindi (हिन्दी)")], default="en")
    submit = SubmitField("Register")

    def validate_password(self, field):
        p = field.data
        if p.isdigit():
            raise ValidationError("Password cannot consist solely of numbers.")
        if p.lower() in ["password", "12345678", "qwerty1234", "admin1234"]:
            raise ValidationError("This password is too common or easily guessed.")


class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class RecommendationForm(FlaskForm):
    region = SelectField("Region / Zone", choices=[], validators=[Optional()])
    soil_type = SelectField(
        "Soil Type",
        choices=[
            ("Alluvial", "Alluvial (River Basin / Delta)"),
            ("Clay", "Clay (High Moisture Retention)"),
            ("Loamy", "Loamy (Balanced Aeration & Fertility)"),
            ("Sandy", "Sandy (Coarse & Well Draining)"),
            ("Black", "Black (Regur / Cotton Soil)"),
            ("Red", "Red (Porous, Iron Rich)"),
        ],
        validators=[DataRequired()],
    )
    season = SelectField(
        "Farming Season",
        choices=[
            ("Kharif", "Kharif (Monsoon: June - October)"),
            ("Rabi", "Rabi (Winter: October - April)"),
            ("Zaid", "Zaid (Summer: March - June)"),
            ("Year-round", "Year-round (Perennial Cultivation)"),
        ],
        validators=[DataRequired()],
    )
    water_availability = SelectField(
        "Water Availability",
        choices=[
            ("High", "High (Canal, River, or Assured Borewell Irrigation)"),
            ("Medium", "Medium (Seasonal Well or Semi-Arid Irrigation)"),
            ("Low", "Low (Rainfed / Dryland / Water Scarce)"),
        ],
        validators=[DataRequired()],
    )
    temperature = FloatField("Ambient Temperature (°C, Optional)", validators=[Optional(), NumberRange(min=-10, max=55)])
    rainfall = FloatField("Expected Rainfall (mm, Optional)", validators=[Optional(), NumberRange(min=0, max=5000)])
    preferred_category = SelectField(
        "Crop Category (Optional)",
        choices=[
            ("All", "All Categories"),
            ("Cereal", "Cereals (Paddy, Wheat, Maize)"),
            ("Pulse", "Pulses & Legumes"),
            ("Vegetable", "Vegetables"),
            ("Fruit", "Fruits"),
            ("Cash Crop", "Cash Crops (Cotton, Sugarcane)"),
            ("Millets", "Nutri-Millets"),
        ],
        default="All",
        validators=[Optional()],
    )
    submit = SubmitField("Calculate Recommendations")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField("Confirm New Password", validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("Update Password")


class ProfileUpdateForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    preferred_language = SelectField("Preferred Language", choices=[("en", "English"), ("ta", "Tamil (தமிழ்)"), ("hi", "Hindi (हिन्दी)")], default="en")
    submit = SubmitField("Save Settings")


# Admin Forms
class AdminCropForm(FlaskForm):
    name = StringField("Crop Name", validators=[DataRequired(), Length(max=100)])
    slug = StringField("Slug (unique)", validators=[DataRequired(), Length(max=80)])
    scientific_name = StringField("Scientific Name", validators=[Optional(), Length(max=120)])
    category = SelectField("Category", choices=[("Cereal", "Cereal"), ("Pulse", "Pulse"), ("Vegetable", "Vegetable"), ("Fruit", "Fruit"), ("Cash Crop", "Cash Crop"), ("Millets", "Millets")], validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    water_requirement = SelectField("Water Requirement", choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")], validators=[DataRequired()])
    season_summary = StringField("Season Summary", validators=[Optional(), Length(max=200)])
    soil_climate_summary = TextAreaField("Soil & Climate Summary", validators=[Optional()])
    image_path = StringField("Image Path / URL", validators=[Optional(), Length(max=255)])
    min_temp = FloatField("Min Temp (°C)", validators=[Optional()])
    max_temp = FloatField("Max Temp (°C)", validators=[Optional()])
    min_rainfall = FloatField("Min Rainfall (mm)", validators=[Optional()])
    max_rainfall = FloatField("Max Rainfall (mm)", validators=[Optional()])
    difficulty_level = SelectField("Difficulty Level", choices=[("Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")], default="Beginner")
    is_published = BooleanField("Published", default=True)
    submit = SubmitField("Save Crop")
