def calculate_macros(weight, target_calories, goal, activity_level):
    """
    Calculate macronutrient breakdown based on body weight,
    target calories, fitness goal, and activity level.

    Returns dict with protein, carbs, fats in grams and percentages.
    """

    goal = goal.lower()
    activity = activity_level.lower()

    # Protein: g per kg of body weight (varies by goal)
    protein_multipliers = {
        "lose weight": 2.0,       # Higher protein to preserve muscle
        "maintain weight": 1.6,   # Moderate protein
        "gain weight": 1.8,       # High protein for muscle gain
    }

    # Adjust protein slightly for very active individuals
    activity_protein_boost = {
        "sedentary": 0.0,
        "lightly active": 0.0,
        "moderately active": 0.1,
        "very active": 0.2,
        "extra active": 0.3,
    }

    base_multiplier = protein_multipliers.get(goal, 1.6)
    boost = activity_protein_boost.get(activity, 0.0)
    protein_per_kg = round(base_multiplier + boost, 2)
    protein_g = round(weight * protein_per_kg, 1)
    protein_cal = protein_g * 4

    # Fat: percentage of total calories (varies by goal)
    fat_percentages = {
        "lose weight": 0.25,
        "maintain weight": 0.30,
        "gain weight": 0.25,
    }

    fat_pct = fat_percentages.get(goal, 0.30)
    fat_cal = target_calories * fat_pct
    fat_g = round(fat_cal / 9, 1)

    # Carbs: remaining calories after protein and fat
    carb_cal = target_calories - protein_cal - fat_cal
    if carb_cal < 0:
        carb_cal = 0
    carb_g = round(carb_cal / 4, 1)

    # Calculate actual percentages
    total_cal = protein_cal + fat_cal + carb_cal
    if total_cal == 0:
        total_cal = 1

    return {
        "protein_g": protein_g,
        "protein_per_kg": protein_per_kg,
        "protein_calories": round(protein_cal, 1),
        "protein_pct": round((protein_cal / total_cal) * 100, 1),
        "carbs_g": carb_g,
        "carbs_calories": round(carb_cal, 1),
        "carbs_pct": round((carb_cal / total_cal) * 100, 1),
        "fats_g": fat_g,
        "fats_calories": round(fat_cal, 1),
        "fats_pct": round((fat_cal / total_cal) * 100, 1),
    }


def get_micronutrient_recommendations(bmi, category, gender, goal):
    """
    Generate micronutrient recommendations based on BMI category,
    gender, and fitness goal.

    Returns a list of important micronutrients with daily targets
    and importance notes.
    """

    gender = gender.lower()
    goal = goal.lower()
    category = category if category else "Normal Weight"

    # Base micronutrient recommendations
    micros = [
        {
            "name": "Vitamin D",
            "amount": "600-1000 IU",
            "unit": "IU/day",
            "importance": "high",
            "sources": "Sunlight, Fortified milk, Eggs, Fish",
            "note": "Essential for calcium absorption & bone health",
        },
        {
            "name": "Calcium",
            "amount": "1000 mg",
            "unit": "mg/day",
            "importance": "high",
            "sources": "Milk, Paneer, Curd, Ragi, Broccoli",
            "note": "Bone density & muscle function",
        },
        {
            "name": "Iron",
            "amount": "18 mg" if gender == "female" else "8 mg",
            "unit": "mg/day",
            "importance": "high" if gender == "female" else "medium",
            "sources": "Spinach, Lentils, Jaggery, Dates",
            "note": "Oxygen transport & energy production",
        },
        {
            "name": "Vitamin B12",
            "amount": "2.4 mcg",
            "unit": "mcg/day",
            "importance": "high",
            "sources": "Milk, Curd, Eggs, Fortified cereals",
            "note": "Nerve function & red blood cell formation",
        },
        {
            "name": "Omega-3",
            "amount": "250-500 mg",
            "unit": "mg/day",
            "importance": "medium",
            "sources": "Flaxseeds, Walnuts, Chia seeds, Fish",
            "note": "Heart health & reduces inflammation",
        },
        {
            "name": "Zinc",
            "amount": "11 mg" if gender == "male" else "8 mg",
            "unit": "mg/day",
            "importance": "medium",
            "sources": "Pumpkin seeds, Chickpeas, Cashews",
            "note": "Immune function & metabolism",
        },
        {
            "name": "Magnesium",
            "amount": "400 mg" if gender == "male" else "310 mg",
            "unit": "mg/day",
            "importance": "medium",
            "sources": "Almonds, Banana, Dark chocolate, Spinach",
            "note": "Muscle recovery & sleep quality",
        },
        {
            "name": "Vitamin C",
            "amount": "90 mg" if gender == "male" else "75 mg",
            "unit": "mg/day",
            "importance": "medium",
            "sources": "Amla, Guava, Orange, Lemon, Capsicum",
            "note": "Immunity & iron absorption",
        },
        {
            "name": "Fiber",
            "amount": "38 g" if gender == "male" else "25 g",
            "unit": "g/day",
            "importance": "high",
            "sources": "Oats, Whole grains, Fruits, Vegetables",
            "note": "Digestive health & satiety",
        },
        {
            "name": "Potassium",
            "amount": "2600-3400 mg",
            "unit": "mg/day",
            "importance": "medium",
            "sources": "Banana, Coconut water, Potato, Spinach",
            "note": "Blood pressure regulation & heart health",
        },
    ]

    # Adjust importance based on BMI category
    if category == "Obese" or category == "Overweight":
        for m in micros:
            if m["name"] == "Fiber":
                m["importance"] = "high"
                m["note"] = "Critical for weight management & satiety"
            if m["name"] == "Omega-3":
                m["importance"] = "high"
                m["note"] = "Reduces inflammation common in higher BMI"
            if m["name"] == "Vitamin D":
                m["importance"] = "high"
                m["note"] = "Often deficient in higher BMI individuals"

    if category == "Underweight":
        for m in micros:
            if m["name"] == "Iron":
                m["importance"] = "high"
                m["note"] = "Critical for energy when underweight"
            if m["name"] == "Calcium":
                m["importance"] = "high"
                m["note"] = "Extra important for bone density"
            if m["name"] == "Vitamin B12":
                m["importance"] = "high"
                m["note"] = "Supports appetite & nutrient absorption"

    # Adjust for goal
    if goal == "gain weight":
        for m in micros:
            if m["name"] == "Zinc":
                m["importance"] = "high"
                m["note"] = "Supports muscle growth & testosterone"
            if m["name"] == "Magnesium":
                m["importance"] = "high"
                m["note"] = "Critical for muscle recovery & protein synthesis"

    if goal == "lose weight":
        for m in micros:
            if m["name"] == "Vitamin C":
                m["importance"] = "high"
                m["note"] = "Fat oxidation & cortisol regulation"
            if m["name"] == "Fiber":
                m["importance"] = "high"
                m["note"] = "Keeps you full & supports fat loss"

    return micros


def generate_health_report(bmi, category, bmr, maintenance_calories,
                            target_calories, weight, height, age,
                            gender, activity_level, goal):
    """
    Generate a comprehensive health report summary with
    key insights and recommendations.
    """

    gender = gender.lower()
    goal = goal.lower()
    height_m = height / 100
    ideal_bmi_low = 18.5
    ideal_bmi_high = 24.9

    ideal_weight_low = round(ideal_bmi_low * (height_m ** 2), 1)
    ideal_weight_high = round(ideal_bmi_high * (height_m ** 2), 1)

    # Weight difference from ideal range
    if weight < ideal_weight_low:
        weight_diff = round(ideal_weight_low - weight, 1)
        weight_status = f"You are {weight_diff} kg below the healthy weight range"
    elif weight > ideal_weight_high:
        weight_diff = round(weight - ideal_weight_high, 1)
        weight_status = f"You are {weight_diff} kg above the healthy weight range"
    else:
        weight_status = "Your weight is within the healthy range"

    # Calorie deficit/surplus info
    calorie_diff = abs(target_calories - maintenance_calories)
    if target_calories < maintenance_calories:
        calorie_info = f"{round(calorie_diff)} kcal daily deficit for weight loss"
        weekly_change = round((calorie_diff * 7) / 7700, 2)
        pace_info = f"~{weekly_change} kg loss per week"
    elif target_calories > maintenance_calories:
        calorie_info = f"{round(calorie_diff)} kcal daily surplus for weight gain"
        weekly_change = round((calorie_diff * 7) / 7700, 2)
        pace_info = f"~{weekly_change} kg gain per week"
    else:
        calorie_info = "Maintenance calories to sustain current weight"
        pace_info = "Weight will remain stable"

    # Body fat estimate (rough formula)
    if gender == "male":
        body_fat_est = round(1.20 * bmi + 0.23 * age - 16.2, 1)
    else:
        body_fat_est = round(1.20 * bmi + 0.23 * age - 5.4, 1)

    if body_fat_est < 0:
        body_fat_est = 5.0

    # Recommendations
    recommendations = []

    if category == "Underweight":
        recommendations.append("Increase calorie intake with nutrient-dense foods")
        recommendations.append("Focus on strength training to build muscle mass")
        recommendations.append("Eat frequent small meals throughout the day")
    elif category == "Overweight":
        recommendations.append("Create a moderate calorie deficit (300-500 kcal)")
        recommendations.append("Increase fiber and protein intake for satiety")
        recommendations.append("Add 150+ minutes of moderate exercise per week")
    elif category == "Obese":
        recommendations.append("Consult a healthcare professional for guidance")
        recommendations.append("Start with low-impact exercises like walking")
        recommendations.append("Focus on whole foods and reduce processed foods")
    else:
        recommendations.append("Maintain your balanced diet and active lifestyle")
        recommendations.append("Focus on nutrient quality over quantity")
        recommendations.append("Stay consistent with your exercise routine")

    if goal == "lose weight":
        recommendations.append("Prioritize protein to preserve lean muscle mass")
    elif goal == "gain weight":
        recommendations.append("Eat calorie-dense foods: nuts, ghee, dried fruits")

    return {
        "ideal_weight_range": f"{ideal_weight_low} - {ideal_weight_high} kg",
        "ideal_weight_low": ideal_weight_low,
        "ideal_weight_high": ideal_weight_high,
        "weight_status": weight_status,
        "calorie_info": calorie_info,
        "pace_info": pace_info,
        "body_fat_estimate": body_fat_est,
        "recommendations": recommendations,
    }
