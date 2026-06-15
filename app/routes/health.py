import math
from datetime import date

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.health_profile import HealthProfile
from app.models.diet_plan import DietPlan
from app.schemas.health_profile_schema import HealthProfileSchema
from app.utils.throttling import throttle_request


from app.services.bmi_service import calculate_bmi
from app.services.calorie_service import calculate_calories
from app.services.diet_service import generate_diet_plan, regenerate_diet_plan
from app.services.water_service import calculate_water_intake
from app.services.nutrition_service import (
    calculate_macros,
    get_micronutrient_recommendations,
    generate_health_report,
)

health_bp = Blueprint("health", __name__)

health_schema = HealthProfileSchema()


def build_profile_response(profile):
    """
    Build the full profile response dict with all calculated data:
    BMI, calories, diet, macros, micros, and health report.
    """

    bmi, category = calculate_bmi(profile.weight, profile.height)

    bmr, maintenance_calories, target_calories = calculate_calories(
        profile.age,
        profile.gender,
        profile.height,
        profile.weight,
        profile.activity_level,
        profile.goal,
    )

    macros = calculate_macros(
        profile.weight,
        target_calories,
        profile.goal,
        profile.activity_level,
    )

    micros = get_micronutrient_recommendations(
        bmi, category, profile.gender, profile.goal
    )

    user_profile = {
        "age": profile.age,
        "gender": profile.gender,
        "height": profile.height,
        "weight": profile.weight,
        "bmi": bmi,
        "category": category,
        "goal": profile.goal,
        "activity_level": profile.activity_level,
        "target_calories": target_calories,
        "diet_type": profile.diet_type,
        "macros": macros,
        "micronutrients": micros,
    }

    # Fetch cached diet plan from database
    diet_plan_record = db.session.query(DietPlan).filter_by(user_id=profile.user_id).first()
    if diet_plan_record:
        diet_plan = diet_plan_record.meal_plan
    else:
        # Generate new diet plan using local fast preset generator
        diet_plan = generate_diet_plan(profile.goal, profile.diet_type, bmi=bmi)
        
        # Save to database cache
        try:
            new_diet_plan_record = DietPlan(
                user_id=profile.user_id,
                daily_calories=int(target_calories),
                protein=macros.get("protein_g"),
                carbs=macros.get("carbs_g"),
                fats=macros.get("fats_g"),
                meal_plan=diet_plan
            )
            db.session.add(new_diet_plan_record)
            db.session.commit()
        except Exception:
            db.session.rollback()

    health_report = generate_health_report(
        bmi, category, bmr, maintenance_calories,
        target_calories, profile.weight, profile.height,
        profile.age, profile.gender, profile.activity_level,
        profile.goal,
    )

    return {
        "user_id": profile.user_id,
        "user_name": profile.user.name if profile.user else None,
        "email": profile.user.email if profile.user else None,
        "profile_photo": f"/static/uploads/{profile.user.profile_photo}" if profile.user and profile.user.profile_photo else None,
        "age": profile.age,
        "gender": profile.gender,
        "height": profile.height,
        "weight": profile.weight,
        "activity_level": profile.activity_level,
        "goal": profile.goal,
        "diet_type": profile.diet_type,
        "bmi": bmi,
        "category": category,
        "bmr": bmr,
        "maintenance_calories": maintenance_calories,
        "target_calories": target_calories,
        "diet_plan": diet_plan,
        "macros": macros,
        "micronutrients": micros,
        "health_report": health_report,
    }


@health_bp.route("/health-profile", methods=["POST"])
@jwt_required()
def create_health_profile():

    try:
        data = health_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_id = int(get_jwt_identity())

    # Update if profile exists, otherwise create new
    profile = db.session.query(HealthProfile).filter_by(user_id=user_id).first()
    if profile:
        updatable_fields = ["age", "gender", "height", "weight", "activity_level", "goal", "diet_type"]
        for field in updatable_fields:
            if field in data:
                setattr(profile, field, data[field])
    else:
        profile = HealthProfile(
            user_id=user_id,
            age=data["age"],
            gender=data["gender"],
            height=data["height"],
            weight=data["weight"],
            activity_level=data["activity_level"],
            goal=data["goal"],
            diet_type=data["diet_type"],
        )
        db.session.add(profile)

    db.session.commit()

    response = build_profile_response(profile)
    response["message"] = "Profile updated successfully" if profile.id else "Health profile created successfully"
    return jsonify(response), 201


@health_bp.route("/health-profile", methods=["GET"])
@jwt_required()
def get_health_profile():

    user_id = int(get_jwt_identity())

    profile = db.session.query(HealthProfile).filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return jsonify({
            "message": "Health profile not found"
        }), 404

    return jsonify(build_profile_response(profile)), 200


@health_bp.route("/health-profile", methods=["PUT"])
@jwt_required()
def update_health_profile():

    user_id = int(get_jwt_identity())

    profile = db.session.query(HealthProfile).filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return jsonify({
            "message": "Health profile not found"
        }), 404

    try:
        data = health_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if not data:
        return jsonify({
            "message": "No fields provided to update"
        }), 400

    # Update only the fields that were provided
    updatable_fields = ["age", "gender", "height", "weight", "activity_level", "goal", "diet_type"]
    for field in updatable_fields:
        if field in data:
            setattr(profile, field, data[field])

    db.session.commit()

    response = build_profile_response(profile)
    response["message"] = "Profile updated successfully"
    return jsonify(response), 200


@health_bp.route("/water-intake", methods=["GET"])
@jwt_required()
def get_water_intake():

    user_id = int(get_jwt_identity())

    profile = db.session.query(HealthProfile).filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return jsonify({
            "message": "Health profile not found"
        }), 404

    bmi, category = calculate_bmi(
        profile.weight,
        profile.height
    )

    base_intake, recommended_intake = calculate_water_intake(
        profile.weight,
        bmi
    )

    return jsonify({
        "weight": profile.weight,
        "bmi": bmi,
        "category": category,
        "base_water_intake_liters": base_intake,
        "recommended_water_intake_liters": recommended_intake
    }), 200


@health_bp.route("/regenerate-diet", methods=["POST"])
@jwt_required()
def regenerate_diet():
    """Generate a new random diet plan variant."""
    user_id = int(get_jwt_identity())

    profile = db.session.query(HealthProfile).filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"message": "Health profile not found"}), 404

    bmi, category = calculate_bmi(profile.weight, profile.height)
    _, _, target_calories = calculate_calories(
        profile.age, profile.gender, profile.height,
        profile.weight, profile.activity_level, profile.goal
    )
    macros = calculate_macros(
        profile.weight, target_calories, profile.goal, profile.activity_level
    )
    micros = get_micronutrient_recommendations(
        bmi, category, profile.gender, profile.goal
    )
    
    user_profile = {
        "age": profile.age,
        "gender": profile.gender,
        "height": profile.height,
        "weight": profile.weight,
        "bmi": bmi,
        "category": category,
        "goal": profile.goal,
        "activity_level": profile.activity_level,
        "target_calories": target_calories,
        "diet_type": profile.diet_type,
        "macros": macros,
        "micronutrients": micros,
    }
    
    # Generate new diet plan variant using local fast preset generator
    new_plan, variant_idx = regenerate_diet_plan(profile.goal, profile.diet_type, bmi=bmi)

    try:
        diet_plan_record = db.session.query(DietPlan).filter_by(user_id=user_id).first()
        if diet_plan_record:
            diet_plan_record.meal_plan = new_plan
            diet_plan_record.daily_calories = int(target_calories)
            diet_plan_record.protein = macros.get("protein_g")
            diet_plan_record.carbs = macros.get("carbs_g")
            diet_plan_record.fats = macros.get("fats_g")
        else:
            diet_plan_record = DietPlan(
                user_id=user_id,
                daily_calories=int(target_calories),
                protein=macros.get("protein_g"),
                carbs=macros.get("carbs_g"),
                fats=macros.get("fats_g"),
                meal_plan=new_plan
            )
            db.session.add(diet_plan_record)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return jsonify({
        "diet_plan": new_plan,
        "variant": variant_idx,
        "goal": profile.goal,
        "message": "New diet plan generated!"
    }), 200