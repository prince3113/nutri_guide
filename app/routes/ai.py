from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.health_profile import HealthProfile
from app.services.bmi_service import calculate_bmi
from app.services.calorie_service import calculate_calories
from app.services.ai_service import chat_with_ai, recognize_food

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"message": "Message is required"}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"message": "Message cannot be empty"}), 400

    user_id = get_jwt_identity()

    # Build user profile context
    user_profile = None
    profile = HealthProfile.query.filter_by(user_id=user_id).first()

    if profile:
        bmi, category = calculate_bmi(profile.weight, profile.height)
        _, _, target_calories = calculate_calories(
            profile.age, profile.gender, profile.height,
            profile.weight, profile.activity_level, profile.goal
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
        }

    response_text = chat_with_ai(user_message, user_profile)

    return jsonify({
        "message": user_message,
        "response": response_text,
    }), 200


@ai_bp.route("/recognize-food", methods=["POST"])
@jwt_required()
def recognize_food_route():
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"message": "Image data is required"}), 400

    image_base64 = data["image"]

    if not image_base64:
        return jsonify({"message": "Image data cannot be empty"}), 400

    result = recognize_food(image_base64)

    if "error" in result:
        return jsonify({"message": result["error"]}), 500

    return jsonify(result), 200
