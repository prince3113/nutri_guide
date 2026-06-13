import math
from datetime import date

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.health_profile import HealthProfile
from app.models.water_log import WaterLog
from app.schemas.health_profile_schema import HealthProfileSchema

from app.services.bmi_service import calculate_bmi
from app.services.calorie_service import calculate_calories
from app.services.diet_service import generate_diet_plan, regenerate_diet_plan
from app.services.ai_service import generate_diet_plan_ai
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

    diet_plan = generate_diet_plan_ai(user_profile)
    if not diet_plan:
        diet_plan = generate_diet_plan(profile.goal, profile.diet_type)

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

    user_id = get_jwt_identity()

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
    response["message"] = "Health profile created successfully"
    return jsonify(response), 201


@health_bp.route("/health-profile", methods=["GET"])
@jwt_required()
def get_health_profile():

    user_id = get_jwt_identity()

    profile = HealthProfile.query.filter_by(
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

    user_id = get_jwt_identity()

    profile = HealthProfile.query.filter_by(
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

    user_id = get_jwt_identity()

    profile = HealthProfile.query.filter_by(
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


@health_bp.route("/water-tracker", methods=["GET"])
@jwt_required()
def get_water_tracker():
    """Get today's water tracking data."""
    user_id = get_jwt_identity()

    profile = HealthProfile.query.filter_by(user_id=user_id).first()

    # Calculate target glasses from recommended water intake
    target_glasses = 8  # default
    if profile:
        bmi, _ = calculate_bmi(profile.weight, profile.height)
        _, recommended = calculate_water_intake(profile.weight, bmi)
        target_glasses = max(1, math.ceil(recommended / 0.25))  # 1 glass = 250ml

    today = date.today()
    log = WaterLog.query.filter_by(user_id=user_id, log_date=today).first()

    if not log:
        log = WaterLog(user_id=user_id, target_glasses=target_glasses)
        db.session.add(log)
        db.session.commit()

    progress = round((log.glasses_consumed / log.target_glasses) * 100, 1) if log.target_glasses > 0 else 0

    return jsonify({
        "glasses_consumed": log.glasses_consumed,
        "target_glasses": log.target_glasses,
        "progress_percent": min(progress, 100),
        "liters_consumed": round(log.glasses_consumed * 0.25, 2),
        "target_liters": round(log.target_glasses * 0.25, 2),
        "date": str(today),
    }), 200


@health_bp.route("/water-tracker/drink", methods=["POST"])
@jwt_required()
def drink_water():
    """Add 1 glass of water to today's log."""
    user_id = get_jwt_identity()
    today = date.today()

    log = WaterLog.query.filter_by(user_id=user_id, log_date=today).first()

    if not log:
        profile = HealthProfile.query.filter_by(user_id=user_id).first()
        target_glasses = 8
        if profile:
            bmi, _ = calculate_bmi(profile.weight, profile.height)
            _, recommended = calculate_water_intake(profile.weight, bmi)
            target_glasses = max(1, math.ceil(recommended / 0.25))
        log = WaterLog(user_id=user_id, target_glasses=target_glasses)
        db.session.add(log)

    log.glasses_consumed += 1
    db.session.commit()

    progress = round((log.glasses_consumed / log.target_glasses) * 100, 1) if log.target_glasses > 0 else 0

    return jsonify({
        "glasses_consumed": log.glasses_consumed,
        "target_glasses": log.target_glasses,
        "progress_percent": min(progress, 100),
        "liters_consumed": round(log.glasses_consumed * 0.25, 2),
        "target_liters": round(log.target_glasses * 0.25, 2),
        "date": str(today),
        "message": "Water logged!"
    }), 200


@health_bp.route("/water-tracker/reset", methods=["POST"])
@jwt_required()
def reset_water():
    """Reset today's water count to 0."""
    user_id = get_jwt_identity()
    today = date.today()

    log = WaterLog.query.filter_by(user_id=user_id, log_date=today).first()
    if log:
        log.glasses_consumed = 0
        db.session.commit()

    return jsonify({
        "glasses_consumed": 0,
        "target_glasses": log.target_glasses if log else 8,
        "progress_percent": 0,
        "liters_consumed": 0,
        "target_liters": round((log.target_glasses if log else 8) * 0.25, 2),
        "date": str(today),
        "message": "Water tracker reset!"
    }), 200


@health_bp.route("/regenerate-diet", methods=["POST"])
@jwt_required()
def regenerate_diet():
    """Generate a new random diet plan variant."""
    user_id = get_jwt_identity()

    profile = HealthProfile.query.filter_by(user_id=user_id).first()
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
    
    new_plan = generate_diet_plan_ai(user_profile)
    variant_idx = "ai"
    
    if not new_plan:
        new_plan, variant_idx = regenerate_diet_plan(profile.goal, profile.diet_type)

    return jsonify({
        "diet_plan": new_plan,
        "variant": variant_idx,
        "goal": profile.goal,
        "message": "New diet plan generated!"
    }), 200