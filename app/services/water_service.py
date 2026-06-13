def calculate_water_intake(weight, bmi):

    base_intake = round(weight * 0.035, 2)

    if bmi >= 30:
        adjustment = 0.5
    elif bmi >= 25:
        adjustment = 0.3
    elif bmi < 18.5:
        adjustment = -0.2
    else:
        adjustment = 0

    recommended_intake = round(
        base_intake + adjustment,
        2
    )

    return base_intake, recommended_intake
