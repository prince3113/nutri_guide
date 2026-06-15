import random

# Diet plan variants categorized by: Goal -> Diet Type (vegetarian/non-vegetarian) -> BMI Category -> List of plans
# Each meal dict keys are strictly ordered: breakfast, lunch, snacks, dinner
DIET_PLANS = {
    "lose weight": {
        "vegetarian": {
            "Underweight": [
                {
                    "breakfast": "Oats with Honey, Chia seeds & Apple 🍎",
                    "lunch": "2 Rotis + Dal Tadka + Sautéed Tofu + Salad 🥗",
                    "snacks": "Handful of Almonds & Raisins + Green Tea 🍵",
                    "dinner": "Paneer Stuffed Roti + Cucumber Raita 🥒"
                },
                {
                    "breakfast": "Moong Dal Chilla with paneer stuffing + Mint Chutney 🌿",
                    "lunch": "Quinoa Salad with Chickpeas, Cucumber & Olive oil 🫒",
                    "snacks": "Banana with 1 tbsp Peanut Butter 🍌",
                    "dinner": "Tofu Stir-fry with Broccoli, Mushroom & Sesame seeds 🥦"
                },
                {
                    "breakfast": "Ragi Dosa + Peanut Chutney 🥜",
                    "lunch": "Multigrain Roti + Lauki Sabzi + Thick Dal 🥣",
                    "snacks": "Roasted Makhana + Apple slices 🍎",
                    "dinner": "Vegetable Soup + Paneer Salad 🧀"
                }
            ],
            "Normal Weight": [
                {
                    "breakfast": "Oats porridge with apple slices 🍎",
                    "lunch": "2 Rotis + Dal + Mixed Green Salad 🥗",
                    "snacks": "Roasted Chana + Green Tea 🍵",
                    "dinner": "Grilled Paneer/Tofu with Steamed Broccoli 🥦"
                },
                {
                    "breakfast": "Besan Chilla + Mint Chutney 🌿",
                    "lunch": "Brown Rice + Rajma + Cucumber Salad 🥒",
                    "snacks": "Sprouts Chaat + Coconut Water 🥥",
                    "dinner": "Vegetable Soup + Paneer Salad 🧀"
                },
                {
                    "breakfast": "Idli + Sambar + Coconut Chutney 🥥",
                    "lunch": "Jowar Roti + Bhindi Sabzi + Curd 🥣",
                    "snacks": "Mixed Seeds + Apple 🍎",
                    "dinner": "Mushroom Stir Fry + Vegetable Soup 🍄"
                }
            ],
            "Overweight": [
                {
                    "breakfast": "Vegetable Oats Porridge (low oil) 🥣",
                    "lunch": "1 Multigrain Roti + Dal + Large Bowl of Green Salad 🥗",
                    "snacks": "Cucumber and Carrot Sticks with Mint Dip 🥕",
                    "dinner": "Grilled Paneer/Tofu with Cauliflower Rice & Veggies 🥦"
                },
                {
                    "breakfast": "Moong Dal Chilla (no oil) + Mint Chutney 🌿",
                    "lunch": "Boiled Chana Salad with Cucumber and Tomato 🍅",
                    "snacks": "Roasted Makhana + Green Tea 🍵",
                    "dinner": "Palak Soup + Sautéed Mushroom & Tofu 🍄"
                },
                {
                    "breakfast": "Sprouts Bowl + Lemon Water 🍋",
                    "lunch": "Vegetable Soup + Sautéed Paneer/Tofu Salad 🥗",
                    "snacks": "Roasted Chickpeas (Garam) 🧆",
                    "dinner": "Methi Roti + Mix Veg Sabzi (low oil) + Curd 🥣"
                }
            ],
            "Obese": [
                {
                    "breakfast": "Light Oats Porridge in water + Apple 🍎",
                    "lunch": "1 Roti + Dal + Large Green Salad with Lemon (No oil) 🥗",
                    "snacks": "Cucumber Slices + Lemon Tea 🍋",
                    "dinner": "Steamed Tofu/Paneer + Broccoli & Carrot Soup 🥕"
                },
                {
                    "breakfast": "Steamed Sprouts with Tomato & Onion (no oil) 🧅",
                    "lunch": "Moong Dal Soup + Sautéed Tofu + Lettuce Salad 🥬",
                    "snacks": "Roasted Makhana (Dry) + Green Tea 🍵",
                    "dinner": "Vegetable Clear Soup + Stir-fried Mushrooms & Bell Peppers 🫑"
                },
                {
                    "breakfast": "Boiled Moong + Mint Chutney 🌿",
                    "lunch": "Boiled Chickpea Salad + Buttermilk 🥛",
                    "snacks": "Papaya slices (small bowl) 🥭",
                    "dinner": "Clear Cauliflower Soup + Sautéed Broccoli and Zucchini 🥒"
                }
            ]
        },
        "non-vegetarian": {
            "Underweight": [
                {
                    "breakfast": "3 Egg Whites Scramble + Whole Wheat Toast + Milk 🥛",
                    "lunch": "Brown Rice + Chicken Curry + Salad 🥗",
                    "snacks": "Mixed Nuts & Seeds + Green Tea 🍵",
                    "dinner": "Grilled Chicken Breast + Steamed Vegetables 🥦"
                },
                {
                    "breakfast": "Oats with Honey & Raisins + 2 Boiled Eggs 🥚",
                    "lunch": "2 Rotis + Dal + Fish Curry + Salad 🥗",
                    "snacks": "Banana with Peanut Butter 🍌",
                    "dinner": "Chicken Keema + Chapati + Cucumber Raita 🥒"
                },
                {
                    "breakfast": "French Toast (low sugar) + 2 Boiled Eggs 🍳",
                    "lunch": "Jeera Rice + Mutton Curry + Salad 🥗",
                    "snacks": "Roasted Chana + Apple 🍎",
                    "dinner": "Grilled Fish + Broccoli & Mushroom Soup 🍄"
                }
            ],
            "Normal Weight": [
                {
                    "breakfast": "Oats + Apple + 2 Egg Whites 🍳",
                    "lunch": "2 Rotis + Dal + Chicken Salad 🥗",
                    "snacks": "Roasted Chana + Green Tea 🍵",
                    "dinner": "Grilled Chicken/Fish + Vegetables 🥦"
                },
                {
                    "breakfast": "Moong Dal Chilla + 2 Egg Whites 🥚",
                    "lunch": "Brown Rice + Fish Curry + Cucumber Salad 🥒",
                    "snacks": "Mixed Seeds + Green Tea 🍵",
                    "dinner": "Palak Soup + Grilled Chicken Breast 🍗"
                },
                {
                    "breakfast": "Idli + Sambar + 2 Boiled Eggs 🥚",
                    "lunch": "Jowar Roti + Bhindi Sabzi + Egg Curry 🍳",
                    "snacks": "Sprouts Chaat + Coconut Water 🥥",
                    "dinner": "Vegetable Soup + Boiled Egg Salad 🥗"
                }
            ],
            "Overweight": [
                {
                    "breakfast": "3 Egg White Omelette with spinach & mushrooms + Green Tea 🍵",
                    "lunch": "1 Multigrain Roti + Dal + Chicken Salad (low dressing) 🥗",
                    "snacks": "Cucumber & Carrot Sticks + Mint Dip 🥕",
                    "dinner": "Grilled Fish + Cauliflower Rice & Steamed Asparagus 🥦"
                },
                {
                    "breakfast": "Oats porridge in water + 2 Boiled Egg Whites 🍳",
                    "lunch": "Boiled Chicken Salad with Cucumber and Tomato 🍅",
                    "snacks": "Roasted Makhana + Green Tea 🍵",
                    "dinner": "Clear Chicken Soup + Stir-fried Broccoli & Tofu 🥦"
                },
                {
                    "breakfast": "Egg White Scramble (no butter) + Lemon Water 🍋",
                    "lunch": "Brown Rice (half cup) + Fish Curry + Large Salad 🥗",
                    "snacks": "Roasted Chickpeas 🧆",
                    "dinner": "Boiled Eggs (no yolk) + Vegetable Soup 🥣"
                }
            ],
            "Obese": [
                {
                    "breakfast": "3 Egg White Scramble + Spinach + Green Tea 🍵",
                    "lunch": "Clear Chicken Soup + Large Green Salad with Lemon 🥗",
                    "snacks": "Cucumber Slices + Lemon Tea 🍋",
                    "dinner": "Steamed Fish + Broccoli & Carrot Soup 🥕"
                },
                {
                    "breakfast": "Boiled Egg Whites + Cucumber & Apple slices 🍎",
                    "lunch": "Sautéed Chicken Breast (no oil) + Lettuce Salad 🥬",
                    "snacks": "Roasted Makhana (Dry) + Green Tea 🍵",
                    "dinner": "Vegetable Clear Soup + Grilled Chicken breast strips 🍗"
                },
                {
                    "breakfast": "Scrambled Egg Whites (spinach, onion) 🥚",
                    "lunch": "Fish Soup + Sautéed Broccoli and Zucchini 🥒",
                    "snacks": "Papaya slices (small bowl) 🥭",
                    "dinner": "Clear Cauliflower Soup + Sautéed Tofu & Mushroom 🍄"
                }
            ]
        }
    },
    "gain weight": {
        "vegetarian": {
            "Underweight": [
                {
                    "breakfast": "Double Banana Shake + 2 Peanut Butter Toast 🍌",
                    "lunch": "Rice + Dal Tadka + Paneer Butter Masala + Salad 🥗",
                    "snacks": "Mixed Dry Fruits (Almonds, Cashews, Dates) + Full-cream Milk 🥛",
                    "dinner": "3 Chapatis + Dal + Paneer Bhurji with Ghee 🧀"
                },
                {
                    "breakfast": "Aloo Paneer Paratha with Curd and Butter 🧈",
                    "lunch": "Veg Biryani + Paneer Tikka + Raita 🥣",
                    "snacks": "Avocado Toast + Mango Shake 🥭",
                    "dinner": "Cheese Pasta with Broccoli + Protein Shake 🥛"
                },
                {
                    "breakfast": "Ragi Dosa with Potato Stuffing + Coconut Chutney 🥥",
                    "lunch": "Rice + Chole + Paneer Tikka + Papad 🫓",
                    "snacks": "Protein Ladoo + Almonds 🥜",
                    "dinner": "Chapati + Mushroom Gravy + Curd 🥣"
                }
            ],
            "Normal Weight": [
                {
                    "breakfast": "Banana Shake + Peanut Butter Toast 🍌",
                    "lunch": "Rice + Dal + Paneer Bhurji 🧀",
                    "dinner": "Chapati + Paneer Curry 🥣",
                    "snacks": "Mixed Nuts & Almonds 🥜"
                },
                {
                    "breakfast": "Aloo Paratha + Curd + Lassi 🥛",
                    "lunch": "Veg Biryani + Raita + Papad 🫓",
                    "snacks": "Dry Fruits + Banana Shake 🍌",
                    "dinner": "Paneer Butter Masala + Naan 🫓"
                },
                {
                    "breakfast": "Stuffed Paratha + Butter + Milk 🥛",
                    "lunch": "Rice + Chole + Paneer Tikka 🧀",
                    "snacks": "Protein Ladoo + Almonds 🥜",
                    "dinner": "Pasta + Cheese + Grilled Veggies 🥦"
                }
            ],
            "Overweight": [
                {
                    "breakfast": "Oats with Milk (no sugar) + 1 Banana 🍌",
                    "lunch": "Brown Rice + Dal + Sautéed Paneer 🧀",
                    "snacks": "Boiled Sprouts Salad 🥗",
                    "dinner": "Grilled Tofu with Steamed Asparagus & Quinoa 🥦"
                },
                {
                    "breakfast": "Scrambled Paneer + 1 Slice Whole Wheat Toast 🍞",
                    "lunch": "Multigrain Roti + Mixed Veg Sabzi + Dal 🥣",
                    "snacks": "Roasted Makhana + Buttermilk 🥛",
                    "dinner": "Moong Dal Chilla + Vegetable Soup 🥣"
                },
                {
                    "breakfast": "Besan Chilla + Mint Chutney 🌿",
                    "lunch": "Jeera Rice + Rajma + Cucumber Salad 🥒",
                    "snacks": "Apple + Walnut halves 🍎",
                    "dinner": "Mushroom Soup + Paneer Salad 🥗"
                }
            ],
            "Obese": [
                {
                    "breakfast": "Oats with protein powder and apple 🍎",
                    "lunch": "Brown Rice (small portion) + Dal + Tofu Salad 🥗",
                    "snacks": "Roasted Makhana + Green Tea 🍵",
                    "dinner": "Clear Cauliflower Soup + Sautéed Broccoli 🥦"
                },
                {
                    "breakfast": "Moong Dal Chilla (no oil/butter) 🌿",
                    "lunch": "Boiled Chana Salad + Cucumber Raita 🥒",
                    "snacks": "Buttermilk + Apple 🥛",
                    "dinner": "Vegetable Soup + Paneer Salad (no fat) 🧀"
                },
                {
                    "breakfast": "Sprouts Bowl + Lemon Water 🍋",
                    "lunch": "1 Multigrain Roti + Dal + Veggies 🥦",
                    "snacks": "Roasted Chana 🧆",
                    "dinner": "Palak Soup + Grilled Tofu 🥗"
                }
            ]
        },
        "non-vegetarian": {
            "Underweight": [
                {
                    "breakfast": "Banana Shake + Peanut Butter Toast + 3 Boiled Eggs 🥚",
                    "lunch": "Rice + Dal + Chicken Butter Masala + Salad 🥗",
                    "snacks": "Mixed Nuts & Seeds + Banana Shake 🍌",
                    "dinner": "Chapati + Chicken Keema + Curd 🥣"
                },
                {
                    "breakfast": "Aloo Paratha + Egg Bhurji + Curd & Butter 🧈",
                    "lunch": "Chicken Biryani + Raita + Chicken Kebab 🍗",
                    "snacks": "Dry Fruits + Protein Shake 🥛",
                    "dinner": "Butter Chicken + Naan + Salad 🥗"
                },
                {
                    "breakfast": "Stuffed Paratha + 3 Eggs + Full-cream Milk 🥛",
                    "lunch": "Rice + Fish Curry + Boiled Egg Salad 🍳",
                    "snacks": "Protein Ladoo + Almonds 🥜",
                    "dinner": "Pasta + Chicken Tikka + Cheese 🧀"
                }
            ],
            "Normal Weight": [
                {
                    "breakfast": "Banana Shake + Peanut Butter Toast + 2 Eggs 🥚",
                    "lunch": "Rice + Dal + Chicken Curry 🍗",
                    "snacks": "Mixed Nuts & Walnuts 🥜",
                    "dinner": "Chapati + Egg Bhurji 🍳"
                },
                {
                    "breakfast": "Aloo Paratha + Egg Bhurji + Lassi 🥛",
                    "lunch": "Chicken Biryani + Raita 🥣",
                    "snacks": "Dry Fruits + Banana Shake 🍌",
                    "dinner": "Butter Chicken + Naan 🫓"
                },
                {
                    "breakfast": "Stuffed Paratha + Eggs + Milk 🥛",
                    "lunch": "Rice + Fish Curry + Salad 🥗",
                    "snacks": "Protein Ladoo + Almonds 🥜",
                    "dinner": "Pasta + Chicken Tikka + Cheese 🧀"
                }
            ],
            "Overweight": [
                {
                    "breakfast": "Oats with Milk (no sugar) + 3 Egg Whites 🍳",
                    "lunch": "Brown Rice + Dal + Sautéed Chicken Breast 🍗",
                    "snacks": "Boiled Sprouts Salad 🥗",
                    "dinner": "Grilled Fish with Steamed Asparagus & Quinoa 🥦"
                },
                {
                    "breakfast": "Scrambled Eggs + 1 Slice Whole Wheat Toast 🍞",
                    "lunch": "Multigrain Roti + Mixed Veg Sabzi + Dal 🥣",
                    "snacks": "Roasted Makhana + Buttermilk 🥛",
                    "dinner": "Moong Dal Chilla + Chicken Soup 🥣"
                },
                {
                    "breakfast": "Besan Chilla + 2 Boiled Egg Whites 🍳",
                    "lunch": "Jeera Rice + Fish Curry + Cucumber Salad 🥒",
                    "snacks": "Apple + Walnut halves 🍎",
                    "dinner": "Chicken Soup + Salad 🥗"
                }
            ],
            "Obese": [
                {
                    "breakfast": "Oats with protein powder and 2 Egg Whites 🍳",
                    "lunch": "Brown Rice (small portion) + Dal + Chicken Breast Salad 🥗",
                    "snacks": "Roasted Makhana + Green Tea 🍵",
                    "dinner": "Clear Chicken Soup + Sautéed Broccoli 🥦"
                },
                {
                    "breakfast": "Egg White Omelette (no butter) 🥚",
                    "lunch": "Boiled Chana Salad + Chicken Strips + Cucumber Raita 🥒",
                    "snacks": "Buttermilk + Apple 🥛",
                    "dinner": "Vegetable Soup + Boiled Eggs (no yolk) 🥚"
                },
                {
                    "breakfast": "Sprouts Bowl + 2 Egg Whites + Lemon Water 🍋",
                    "lunch": "1 Multigrain Roti + Dal + Chicken Salad 🥗",
                    "snacks": "Roasted Chana 🧆",
                    "dinner": "Fish Soup + Steamed Veggies 🥦"
                }
            ]
        }
    },
    "maintain weight": {
        "vegetarian": {
            "Underweight": [
                {
                    "breakfast": "Banana Oats Smoothie with Honey 🍌",
                    "lunch": "2 Rotis + Dal + Paneer Curry + Salad 🥗",
                    "snacks": "Walnuts and Figs + Milk 🥛",
                    "dinner": "Vegetable Pulao + Curd + Salad 🥗"
                },
                {
                    "breakfast": "Moong Dal Chilla with paneer + Fruit Bowl 🍉",
                    "lunch": "Rice + Chole Curry + Curd + Papad 🫓",
                    "snacks": "Avocado Toast + Green Tea 🍵",
                    "dinner": "Mushroom Stir Fry + Paneer Roti 🧀"
                }
            ],
            "Normal Weight": [
                {
                    "breakfast": "Poha with peanuts + Green Tea 🍵",
                    "lunch": "2 Rotis + Dal + Mix Veg Sabzi + Salad 🥗",
                    "snacks": "Fruit Bowl (Apple & Papaya) 🍎",
                    "dinner": "Chapati + Sautéed Paneer + Raita 🥒"
                },
                {
                    "breakfast": "Upma with veggies + Buttermilk 🥛",
                    "lunch": "Brown Rice + Dal + Curd + Salad 🥗",
                    "snacks": "Yogurt with Granola 🥣",
                    "dinner": "Khichdi + Sautéed Broccoli 🥦"
                },
                {
                    "breakfast": "Besan Chilla + Green Chutney 🌿",
                    "lunch": "Jeera Rice + Kadhi + Salad 🥗",
                    "snacks": "Banana + Walnuts 🍌",
                    "dinner": "Roti + Aloo Gobi + Raita 🥣"
                }
            ],
            "Overweight": [
                {
                    "breakfast": "Dalia with milk (no sugar) 🥛",
                    "lunch": "1 Roti + Dal + Bowl of Mix Veg + Cucumber Salad 🥗",
                    "snacks": "Roasted Chana + Green Tea 🍵",
                    "dinner": "Palak Paneer (low fat) + Soup 🥣"
                },
                {
                    "breakfast": "Besan Chilla + Mint Chutney 🌿",
                    "lunch": "Quinoa Salad with Paneer/Tofu 🥗",
                    "snacks": "Buttermilk + Roasted Makhana 🥛",
                    "dinner": "Grilled Veggies + Tomato Soup 🍅"
                },
                {
                    "breakfast": "Oats Porridge in water + Apple 🍎",
                    "lunch": "Brown Rice + Mix Veg Dal + Sprout Salad 🥗",
                    "snacks": "Apple + Almonds 🥜",
                    "dinner": "Mushroom Soup + Tofu Salad 🥗"
                }
            ],
            "Obese": [
                {
                    "breakfast": "Vegetable Oats Porridge (low oil) 🥣",
                    "lunch": "1 Roti + Plain Dal + Large Cucumber Salad 🥒",
                    "snacks": "Roasted Makhana (Dry) + Green Tea 🍵",
                    "dinner": "Clear Vegetable Soup + Steamed Broccoli & Tofu 🥦"
                },
                {
                    "breakfast": "Sprouts Salad with Lemon + Coconut Water 🥥",
                    "lunch": "Sautéed Tofu + Vegetable Broth + Lettuce Salad 🥬",
                    "snacks": "Buttermilk 🥛",
                    "dinner": "Clear Cauliflower Soup + Sautéed Mushrooms 🍄"
                }
            ]
        },
        "non-vegetarian": {
            "Underweight": [
                {
                    "breakfast": "Banana Oats Smoothie + 2 Boiled Eggs 🥚",
                    "lunch": "2 Rotis + Dal + Chicken Curry + Salad 🥗",
                    "snacks": "Walnuts and Figs + Milk 🥛",
                    "dinner": "Chicken Pulao + Curd + Salad 🥗"
                },
                {
                    "breakfast": "French Toast + Fruit Bowl 🍉",
                    "lunch": "Rice + Fish Curry + Curd + Salad 🥗",
                    "snacks": "Avocado Toast + Green Tea 🍵",
                    "dinner": "Egg Curry + Roti + Raita 🍳"
                }
            ],
            "Normal Weight": [
                {
                    "breakfast": "Poha with peanuts + 2 Boiled Eggs 🥚",
                    "lunch": "2 Rotis + Dal + Chicken Salad 🥗",
                    "snacks": "Fruit Bowl (Apple & Papaya) 🍎",
                    "dinner": "Chapati + Chicken Stir Fry + Raita 🥒"
                },
                {
                    "breakfast": "Egg Omelette + Toast + Tea 🍳",
                    "lunch": "Roti + Chicken Curry + Rice + Salad 🥗",
                    "snacks": "Yogurt + Granola 🥣",
                    "dinner": "Fish Curry + Rice 🐟"
                },
                {
                    "breakfast": "Besan Chilla + Boiled Eggs 🥚",
                    "lunch": "Jeera Rice + Egg Curry + Salad 🥗",
                    "snacks": "Banana + Walnuts 🍌",
                    "dinner": "Roti + Chicken Kebab + Raita 🍗"
                }
            ],
            "Overweight": [
                {
                    "breakfast": "Dalia with milk (no sugar) + 2 Egg Whites 🍳",
                    "lunch": "1 Roti + Dal + Chicken Breast Salad 🥗",
                    "snacks": "Roasted Chana + Green Tea 🍵",
                    "dinner": "Grilled Fish + Tomato Soup 🍅"
                },
                {
                    "breakfast": "Egg White Omelette + Mint Chutney 🌿",
                    "lunch": "Quinoa Salad with Chicken/Tofu 🥗",
                    "snacks": "Buttermilk + Roasted Makhana 🥛",
                    "dinner": "Grilled Veggies + Chicken Broth 🥣"
                },
                {
                    "breakfast": "Oats Porridge in water + 2 Egg Whites 🥚",
                    "lunch": "Brown Rice + Fish Curry + Sprout Salad 🥗",
                    "snacks": "Apple + Almonds 🥜",
                    "dinner": "Mushroom Soup + Chicken Salad 🥗"
                }
            ],
            "Obese": [
                {
                    "breakfast": "Egg White Scramble (spinach, onion) 🥚",
                    "lunch": "Clear Chicken Soup + Large Cucumber Salad 🥒",
                    "snacks": "Roasted Makhana (Dry) + Green Tea 🍵",
                    "dinner": "Stir-fried Broccoli & Chicken Breast strips 🍗"
                },
                {
                    "breakfast": "Steamed sprouts + 2 Egg Whites + Tea 🍵",
                    "lunch": "Sautéed Chicken + Vegetable Broth + Lettuce Salad 🥬",
                    "snacks": "Buttermilk 🥛",
                    "dinner": "Clear Fish Soup + Sautéed Mushrooms 🍄"
                }
            ]
        }
    }
}


def get_bmi_category(bmi):
    if bmi is None:
        return "Normal Weight"
    
    if isinstance(bmi, str):
        cat = bmi.lower()
        if "under" in cat:
            return "Underweight"
        if "normal" in cat:
            return "Normal Weight"
        if "over" in cat:
            return "Overweight"
        if "obese" in cat:
            return "Obese"
        return "Normal Weight"
        
    elif isinstance(bmi, (int, float)):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal Weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
            
    return "Normal Weight"


def generate_diet_plan(goal, diet_type="vegetarian", bmi=None, variant=None):
    """
    Generate a diet plan based on goal, diet type, and BMI category.
    """
    goal = goal.lower()
    diet_type = diet_type.lower() if diet_type else "vegetarian"
    if diet_type not in ["vegetarian", "non-vegetarian"]:
        diet_type = "vegetarian"

    bmi_cat = get_bmi_category(bmi)
    
    goal_plans = DIET_PLANS.get(goal, DIET_PLANS["maintain weight"])
    type_plans = goal_plans.get(diet_type, goal_plans["vegetarian"])
    plans = type_plans.get(bmi_cat, type_plans["Normal Weight"])

    if variant is not None:
        idx = variant % len(plans)
        return plans[idx]

    return plans[0]


def regenerate_diet_plan(goal, diet_type="vegetarian", bmi=None):
    """
    Generate a random diet plan variant (not the first/default one) matching the user's BMI category.
    """
    goal = goal.lower()
    diet_type = diet_type.lower() if diet_type else "vegetarian"
    if diet_type not in ["vegetarian", "non-vegetarian"]:
        diet_type = "vegetarian"

    bmi_cat = get_bmi_category(bmi)
    
    goal_plans = DIET_PLANS.get(goal, DIET_PLANS["maintain weight"])
    type_plans = goal_plans.get(diet_type, goal_plans["vegetarian"])
    plans = type_plans.get(bmi_cat, type_plans["Normal Weight"])

    if len(plans) > 1:
        idx = random.randint(1, len(plans) - 1)
        return plans[idx], idx
    return plans[0], 0