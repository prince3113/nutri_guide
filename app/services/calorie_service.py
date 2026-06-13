def calculate_calories(
    age,
    gender,
    height,
    weight,
    activity_level,
    goal
):

    if gender.lower() == "male":
        bmr = round(
            10 * weight +
            6.25 * height -
            5 * age + 5,
            2
        )
    else:
        bmr = round(
            10 * weight +
            6.25 * height -
            5 * age - 161,
            2
        )

    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }

    maintenance = round(
        bmr * activity_multipliers.get(
            activity_level.lower(),
            1.2
        ),
        2
    )

    target = maintenance

    if goal.lower() == "lose weight":
        target -= 500
    elif goal.lower() == "gain weight":
        target += 500

    return bmr, maintenance, target