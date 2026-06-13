def calculate_bmi(weight, height):
    height_m = height / 100

    bmi = round(
        weight / (height_m ** 2),
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

    return bmi, category