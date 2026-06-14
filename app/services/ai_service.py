import requests
import json
import time
from flask import current_app

def make_post_request_with_retry(url, json_payload, headers=None, timeout=30, max_retries=3, initial_delay=2):
    """
    Makes a POST request and retries with exponential backoff if a 429 Too Many Requests status is returned.
    """
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=json_payload, headers=headers, timeout=timeout)
            if response.status_code == 429:
                time.sleep(delay)
                delay *= 2
                continue
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay)
            delay *= 2
    
    # Fallback/final request
    return requests.post(url, json=json_payload, headers=headers, timeout=timeout)


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
def get_local_fallback_response(message):
    msg = message.lower().strip()
    
    if "mango" in msg:
        return "Yes, you can eat mangoes during weight loss, but in moderation! 🥭 One medium mango contains about 150-200 calories, so control your portions. It provides excellent fiber and vitamin C, but is high in natural sugars. Enjoying half a mango as a mid-day snack is perfectly fine! 😊"
    
    if "protein" in msg or "breakfast" in msg:
        return "Here are some excellent high-protein breakfast ideas: 🍳\n1. Scrambled Eggs or Paneer Bhurji with whole wheat toast.\n2. Moong Dal Chilla stuffed with low-fat paneer.\n3. Greek Yogurt bowl topped with almonds, pumpkin seeds, and a scoop of protein powder.\n4. Oatmeal made with milk, chia seeds, and protein powder."
        
    if "workout" in msg or "pre" in msg or "exercise" in msg:
        return "For a great pre-workout meal, focus on easy-to-digest carbs and protein 30-60 minutes before: 🍌\n1. A banana with 1 tbsp of peanut butter.\n2. Whole wheat toast with 2 boiled egg whites.\n3. A small bowl of oatmeal with berries.\nAvoid very heavy, high-fat, or high-fiber foods to prevent stomach discomfort during your workout!"

    return "I'm NutriGuide AI. The remote AI service is currently busy, but remember to prioritize balanced meals with lean protein, fiber-rich vegetables, complex carbohydrates, and plenty of hydration! 🥗💧 Please try asking your question again in a minute."

def chat_with_ai(message, user_profile=None):
    """
    Send a nutrition question to OpenAI and get a response.
    """
    api_key = current_app.config.get("OPENAI_API_KEY")
    if not api_key or api_key.strip() in ("", "your_key_here"):
        fallback = get_local_fallback_response(message)
        return f"{fallback}\n\n*(Note: OpenAI API key is not configured, showing local guideline answers)*"

    # Build system context
    if user_profile:
        system_prompt = NUTRITION_SYSTEM_PROMPT.format(**user_profile)
    else:
        system_prompt = "You are NutriGuide AI, a friendly nutrition assistant. Give concise, practical answers about diet and nutrition."

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = make_post_request_with_retry(url, payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Extract text from OpenAI response
        choices = data.get("choices", [])
        if choices:
            content = choices[0].get("message", {}).get("content", "")
            if content:
                return content.strip()

        return "Sorry, I couldn't generate a response. Please try again."

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else None
        if status_code == 429:
            local_ans = get_local_fallback_response(message)
            return f"{local_ans}\n\n*(Note: Remote AI is currently busy, showing local guideline answers)*"
        if status_code in (401, 403):
            return "Invalid OpenAI API Key. Please provide a valid key in your .env file."
        return f"HTTP error occurred (Status {status_code or 'unknown'})"
    except requests.exceptions.Timeout:
        return "The AI service is taking too long. Please try again."
    except requests.exceptions.RequestException as e:
        status_code = e.response.status_code if e.response is not None else None
        if status_code == 429:
            local_ans = get_local_fallback_response(message)
            return f"{local_ans}\n\n*(Note: Remote AI is currently busy, showing local guideline answers)*"
        if status_code in (401, 403):
            return "Invalid OpenAI API Key or unauthorized request. Please check your .env file."
        return f"Error connecting to AI service. Please check your network connection."
    except Exception as e:
        return "An unexpected error occurred while communicating with the AI service. Please try again."


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
    Generate a personalized diet plan using OpenAI based on the user's detailed health profile, macros, and micros.
    """
    api_key = current_app.config.get("OPENAI_API_KEY")
    if not api_key or api_key.strip() in ("", "your_key_here"):
        return None

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

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
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": formatted_prompt},
            {"role": "user", "content": "Generate my personalized diet plan now in JSON format."}
        ],
        "temperature": 0.5,
        "response_format": {"type": "json_object"}
    }

    try:
        response = make_post_request_with_retry(url, payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        choices = data.get("choices", [])
        if choices:
            content = choices[0].get("message", {}).get("content", "").strip()
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                if content.startswith("```"):
                    content = content.split("\n", 1)[1] if "\n" in content else content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return None
        return None
    except Exception:
        return None
