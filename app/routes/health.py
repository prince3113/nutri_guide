from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app import db
from app.models.health_profile import HealthProfile
from app.schemas.health_profile_schema import HealthProfileSchema

health_bp = Blueprint("health", __name__)

health_schema = HealthProfileSchema()


def generate_diet_plan(goal):

    goal = goal.lower()

    if goal == "lose weight":
        return {
            "breakfast": "Oats + Apple + Green Tea",
            "lunch": "2 Rotis + Dal + Salad",
            "dinner": "Grilled Paneer + Vegetables",
            "snacks": "Roasted Chana"
        }

    elif goal == "gain weight":
        return {
            "breakfast": "Banana Shake + Peanut Butter Toast",
            "lunch": "Rice + Dal + Paneer",
            "dinner": "Chapati + Paneer Curry",
            "snacks": "Mixed Nuts"
        }

    else:
        return {
            "breakfast": "Poha + Milk",
            "lunch": "Dal + Rice + Salad",
            "dinner": "Chapati + Vegetables",
            "snacks": "Fruit Bowl"
        }


@health_bp.route("/health-profile", methods=["POST"])
def create_health_profile():

    try:
        data = health_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_id = 1

    # BMI
    height_m = data["height"] / 100

    bmi = round(
        data["weight"] / (height_m ** 2),
        2
    )

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal Weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    # BMR
    if data["gender"].lower() == "male":
        bmr = round(
            10 * data["weight"]
            + 6.25 * data["height"]
            - 5 * data["age"]
            + 5,
            2
        )
    else:
        bmr = round(
            10 * data["weight"]
            + 6.25 * data["height"]
            - 5 * data["age"]
            - 161,
            2
        )

    # Activity Multipliers
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }

    multiplier = activity_multipliers.get(
        data["activity_level"].lower(),
        1.2
    )

    maintenance_calories = round(
        bmr * multiplier,
        2
    )

    target_calories = maintenance_calories

    goal = data["goal"].lower()

    if goal == "lose weight":
        target_calories -= 500
    elif goal == "gain weight":
        target_calories += 500

    # Save Profile
    profile = HealthProfile(
        user_id=user_id,
        age=data["age"],
        gender=data["gender"],
        height=data["height"],
        weight=data["weight"],
        activity_level=data["activity_level"],
        goal=data["goal"]
    )

    db.session.add(profile)
    db.session.commit()

    diet_plan = generate_diet_plan(data["goal"])

    return jsonify({
        "message": "Health profile created successfully",
        "bmi": bmi,
        "category": category,
        "bmr": bmr,
        "maintenance_calories": maintenance_calories,
        "target_calories": target_calories,
        "diet_plan": diet_plan
    }), 201