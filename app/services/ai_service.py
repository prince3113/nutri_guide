import requests
import json
import base64
from flask import current_app


NUTRITION_SYSTEM_PROMPT = """You are NutriGuide AI, a friendly and knowledgeable nutrition assistant.
You help users with diet, nutrition, and health-related questions.

User's Health Profile:
- Age: {age}, Gender: {gender}
- Height: {height} cm, Weight: {weight} kg
- BMI: {bmi} ({category})
- Goal: {goal}
- Activity Level: {activity_level}
- Target Calories: {target_calories} kcal/day

Guidelines:
- Give concise, practical answers (2-4 sentences)
- Focus on Indian diet context when relevant
- Include specific numbers (calories, protein grams) when asked
- Be encouraging and supportive
- If asked about medical conditions, recommend consulting a doctor
- Use emoji occasionally to be friendly
"""

FOOD_RECOGNITION_PROMPT = """Analyze this food image and provide the following information in JSON format:
{
    "food_name": "Name of the food item(s)",
    "description": "Brief description of the dish",
    "estimated_calories": <number>,
    "estimated_protein_g": <number>,
    "estimated_carbs_g": <number>,
    "estimated_fats_g": <number>,
    "serving_size": "approximate serving size",
    "health_rating": "healthy/moderate/unhealthy",
    "tips": "One brief tip about this food"
}

Be as accurate as possible with calorie estimates. If multiple food items are visible, provide totals.
Return ONLY valid JSON, no other text."""


def chat_with_ai(message, user_profile=None):
    """
    Send a nutrition question to Google Gemini and get a response.
    """
    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        return "AI assistant is not configured. Please set GEMINI_API_KEY in your config."

    # Build system context
    if user_profile:
        system_prompt = NUTRITION_SYSTEM_PROMPT.format(**user_profile)
    else:
        system_prompt = "You are NutriGuide AI, a friendly nutrition assistant. Give concise, practical answers about diet and nutrition."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"{system_prompt}\n\nUser question: {message}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500,
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Extract text from Gemini response
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "Sorry, I couldn't generate a response.")

        return "Sorry, I couldn't generate a response. Please try again."

    except requests.exceptions.Timeout:
        return "The AI service is taking too long. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error connecting to AI service: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def recognize_food(image_base64):
    """
    Send a food image to Google Gemini Vision and get nutrition analysis.
    """
    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        return {
            "error": "AI assistant is not configured. Please set GEMINI_API_KEY in your config."
        }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Remove data URI prefix if present
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": image_base64
                        }
                    },
                    {
                        "text": FOOD_RECOGNITION_PROMPT
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 500,
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                text = parts[0].get("text", "")
                # Try to parse JSON from the response
                # Strip markdown code block if present
                text = text.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()

                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {
                        "food_name": "Unknown",
                        "description": text,
                        "estimated_calories": 0,
                        "estimated_protein_g": 0,
                        "estimated_carbs_g": 0,
                        "estimated_fats_g": 0,
                        "serving_size": "Unknown",
                        "health_rating": "moderate",
                        "tips": "Could not parse nutrition data."
                    }

        return {"error": "Could not analyze the image. Please try again."}

    except requests.exceptions.Timeout:
        return {"error": "The AI service is taking too long. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error connecting to AI service: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


DIET_PLAN_SYSTEM_PROMPT = """You are a professional clinical nutritionist.
Generate a realistic and healthy daily diet plan (with Breakfast, Lunch, Dinner, Snacks) tailored specifically for the user's details.

User Profile:
- Age: {age}, Gender: {gender}
- Height: {height} cm, Weight: {weight} kg
- BMI: {bmi} ({category})
- Fitness Goal: {goal}
- Activity Level: {activity_level}
- Target Daily Calories: {target_calories} kcal
- Diet Type: {diet_type} (IMPORTANT: Do NOT include any non-vegetarian ingredients like chicken, egg, meat, fish if the diet type is 'vegetarian'!)

Nutrition Targets:
- Target Macros: Protein: {protein_g}g, Carbs: {carbs_g}g, Fats: {fats_g}g
- Target Micronutrients to focus on: {micros}

Rules:
1. Focus on practical Indian dishes/meals when appropriate (e.g., rotis, dals, upma, paneer, chicken breast, salad, brown rice).
2. The meals must align with the target daily calories and cover the macro requirements.
3. Return ONLY a valid JSON object matching the following structure, without markdown code formatting blocks (no ```json):
{{
    "breakfast": "detailed breakfast description (e.g., 2 egg whites omelette + 1 slice whole wheat toast)",
    "lunch": "detailed lunch description",
    "dinner": "detailed dinner description",
    "snacks": "detailed snacks description"
}}
Do not write any introductory or concluding text, return ONLY the raw JSON object."""


def generate_diet_plan_ai(user_profile):
    """
    Generate a personalized diet plan using Google Gemini based on the user's detailed health profile, macros, and micros.
    """
    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    formatted_prompt = DIET_PLAN_SYSTEM_PROMPT.format(
        age=user_profile.get("age"),
        gender=user_profile.get("gender"),
        height=user_profile.get("height"),
        weight=user_profile.get("weight"),
        bmi=user_profile.get("bmi"),
        category=user_profile.get("category"),
        goal=user_profile.get("goal"),
        activity_level=user_profile.get("activity_level"),
        target_calories=user_profile.get("target_calories"),
        diet_type=user_profile.get("diet_type"),
        protein_g=user_profile.get("macros", {}).get("protein_g", 0),
        carbs_g=user_profile.get("macros", {}).get("carbs_g", 0),
        fats_g=user_profile.get("macros", {}).get("fats_g", 0),
        micros=", ".join([m.get("name") for m in user_profile.get("micronutrients", [])])
    )

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": formatted_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 800,
            "responseMimeType": "application/json"
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                text = parts[0].get("text", "").strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return None
        return None
    except Exception:
        return None
