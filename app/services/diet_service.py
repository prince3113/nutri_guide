import random

# Multiple diet plan variants per goal, split by diet type (vegetarian / non-vegetarian)
DIET_PLANS = {
    "lose weight": {
        "vegetarian": [
            {
                "breakfast": "Oats + Apple + Green Tea",
                "lunch": "2 Rotis + Dal + Salad",
                "dinner": "Grilled Paneer + Vegetables",
                "snacks": "Roasted Chana"
            },
            {
                "breakfast": "Moong Dal Chilla + Mint Chutney",
                "lunch": "Brown Rice + Rajma + Cucumber Raita",
                "dinner": "Palak Soup + Grilled Tofu",
                "snacks": "Mixed Seeds + Green Tea"
            },
            {
                "breakfast": "Idli + Sambar + Coconut Chutney",
                "lunch": "Jowar Roti + Bhindi Sabzi + Curd",
                "dinner": "Vegetable Soup + Paneer Salad",
                "snacks": "Sprouts Chaat"
            },
            {
                "breakfast": "Poha + Lemon Water",
                "lunch": "Quinoa Pulao + Raita + Salad",
                "dinner": "Grilled Paneer + Steamed Veggies",
                "snacks": "Roasted Makhana"
            },
            {
                "breakfast": "Ragi Dosa + Peanut Chutney",
                "lunch": "Multigrain Roti + Lauki Sabzi + Dal",
                "dinner": "Mushroom Stir Fry + Soup",
                "snacks": "Apple + Peanut Butter"
            }
        ],
        "non-vegetarian": [
            {
                "breakfast": "Oats + Apple + Green Tea",
                "lunch": "2 Rotis + Dal + Salad",
                "dinner": "Grilled Paneer/Chicken + Vegetables",
                "snacks": "Roasted Chana"
            },
            {
                "breakfast": "Moong Dal Chilla + Mint Chutney",
                "lunch": "Brown Rice + Rajma + Cucumber Raita",
                "dinner": "Palak Soup + Grilled Chicken",
                "snacks": "Mixed Seeds + Green Tea"
            },
            {
                "breakfast": "Idli + Sambar + Coconut Chutney",
                "lunch": "Jowar Roti + Bhindi Sabzi + Curd",
                "dinner": "Vegetable Soup + Boiled Egg Salad",
                "snacks": "Sprouts Chaat"
            },
            {
                "breakfast": "Poha + Lemon Water",
                "lunch": "Quinoa Pulao + Raita + Salad",
                "dinner": "Grilled Fish + Steamed Veggies",
                "snacks": "Roasted Makhana"
            },
            {
                "breakfast": "Ragi Dosa + Peanut Chutney",
                "lunch": "Multigrain Roti + Chicken Breast + Dal",
                "dinner": "Boiled Eggs + Soup",
                "snacks": "Apple + Peanut Butter"
            }
        ]
    },
    "gain weight": {
        "vegetarian": [
            {
                "breakfast": "Banana Shake + Peanut Butter Toast",
                "lunch": "Rice + Dal + Paneer Bhurji",
                "dinner": "Chapati + Paneer Curry",
                "snacks": "Mixed Nuts"
            },
            {
                "breakfast": "Aloo Paratha + Curd + Lassi",
                "lunch": "Veg Biryani + Raita + Papad",
                "dinner": "Paneer Butter Masala + Naan",
                "snacks": "Dry Fruits + Banana Shake"
            },
            {
                "breakfast": "Stuffed Paratha + Butter + Milk",
                "lunch": "Rice + Chole + Paneer Tikka",
                "dinner": "Pasta + Cheese + Grilled Veggies",
                "snacks": "Protein Ladoo + Almonds"
            },
            {
                "breakfast": "Veg Pancakes + Honey + Milk",
                "lunch": "Jeera Rice + Dal Makhani + Salad",
                "dinner": "Paneer Tikka + Roti",
                "snacks": "Chikki + Mango Shake"
            },
            {
                "breakfast": "Masala Dosa + Potato Filling + Coffee",
                "lunch": "Pulao + Soya Curry + Curd",
                "dinner": "Chapati + Mushroom Gravy",
                "snacks": "Dates + Cashews + Milk"
            }
        ],
        "non-vegetarian": [
            {
                "breakfast": "Banana Shake + Peanut Butter Toast",
                "lunch": "Rice + Dal + Chicken Curry",
                "dinner": "Chapati + Egg Bhurji",
                "snacks": "Mixed Nuts"
            },
            {
                "breakfast": "Aloo Paratha + Egg Bhurji + Lassi",
                "lunch": "Chicken Biryani + Raita",
                "dinner": "Butter Chicken + Naan",
                "snacks": "Dry Fruits + Banana Shake"
            },
            {
                "breakfast": "Stuffed Paratha + Eggs + Milk",
                "lunch": "Rice + Fish Curry + Salad",
                "dinner": "Pasta + Chicken Tikka + Cheese",
                "snacks": "Protein Ladoo + Almonds"
            },
            {
                "breakfast": "French Toast + Eggs + Milk",
                "lunch": "Jeera Rice + Mutton Curry + Salad",
                "dinner": "Egg Curry + Roti",
                "snacks": "Chikki + Mango Shake"
            },
            {
                "breakfast": "Masala Dosa + Boiled Eggs + Coffee",
                "lunch": "Pulao + Chicken Butter Gravy + Curd",
                "dinner": "Chapati + Chicken Keema",
                "snacks": "Dates + Cashews + Milk"
            }
        ]
    },
    "maintain weight": {
        "vegetarian": [
            {
                "breakfast": "Poha + Milk",
                "lunch": "Dal + Rice + Salad",
                "dinner": "Chapati + Vegetables",
                "snacks": "Fruit Bowl"
            },
            {
                "breakfast": "Upma + Coconut Chutney + Tea",
                "lunch": "Roti + Mix Veg + Dal + Rice",
                "dinner": "Khichdi + Papad + Pickle",
                "snacks": "Yogurt + Granola"
            },
            {
                "breakfast": "Besan Chilla + Green Chutney",
                "lunch": "Jeera Rice + Kadhi + Salad",
                "dinner": "Roti + Aloo Gobi + Raita",
                "snacks": "Banana + Walnuts"
            },
            {
                "breakfast": "Dalia + Fruits + Milk",
                "lunch": "Rice + Sambar + Beans Poriyal",
                "dinner": "Chapati + Palak Paneer",
                "snacks": "Roasted Peanuts + Buttermilk"
            },
            {
                "breakfast": "Paneer Bhurji + Toast",
                "lunch": "Curd Rice + Pickle + Papad",
                "dinner": "Vegetable Pulao + Raita",
                "snacks": "Fruit Chaat + Green Tea"
            }
        ],
        "non-vegetarian": [
            {
                "breakfast": "Poha + Milk",
                "lunch": "Dal + Rice + Egg Salad",
                "dinner": "Chapati + Chicken Stir Fry",
                "snacks": "Fruit Bowl"
            },
            {
                "breakfast": "Egg Omelette + Toast + Tea",
                "lunch": "Roti + Chicken Curry + Rice",
                "dinner": "Fish Curry + Rice",
                "snacks": "Yogurt + Granola"
            },
            {
                "breakfast": "Besan Chilla + Boiled Eggs",
                "lunch": "Jeera Rice + Egg Curry + Salad",
                "dinner": "Roti + Chicken Kebab + Raita",
                "snacks": "Banana + Walnuts"
            },
            {
                "breakfast": "Dalia + Fruits + Milk",
                "lunch": "Rice + Sambar + Boiled Egg",
                "dinner": "Chapati + Grilled Chicken",
                "snacks": "Roasted Peanuts + Buttermilk"
            },
            {
                "breakfast": "Egg Bhurji + Toast",
                "lunch": "Chicken Pulao + Raita",
                "dinner": "Roti + Egg Curry",
                "snacks": "Fruit Chaat + Green Tea"
            }
        ]
    }
}


def generate_diet_plan(goal, diet_type="vegetarian", variant=None):
    """
    Generate a diet plan based on goal and diet type.
    """
    goal = goal.lower()
    diet_type = diet_type.lower() if diet_type else "vegetarian"
    if diet_type not in ["vegetarian", "non-vegetarian"]:
        diet_type = "vegetarian"

    goal_plans = DIET_PLANS.get(goal, DIET_PLANS["maintain weight"])
    plans = goal_plans.get(diet_type, goal_plans["vegetarian"])

    if variant is not None:
        idx = variant % len(plans)
        return plans[idx]

    return plans[0]


def regenerate_diet_plan(goal, diet_type="vegetarian"):
    """
    Generate a random diet plan variant (not the first/default one).
    """
    goal = goal.lower()
    diet_type = diet_type.lower() if diet_type else "vegetarian"
    if diet_type not in ["vegetarian", "non-vegetarian"]:
        diet_type = "vegetarian"

    goal_plans = DIET_PLANS.get(goal, DIET_PLANS["maintain weight"])
    plans = goal_plans.get(diet_type, goal_plans["vegetarian"])

    if len(plans) > 1:
        idx = random.randint(1, len(plans) - 1)
        return plans[idx], idx
    return plans[0], 0