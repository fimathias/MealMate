import pandas as pd
import re

data_DB = pd.read_csv("Food_DB.csv")

data_dinner = data_DB[pd.isnull(data_DB["Lunch"])]
data_lunch = data_DB[data_DB["Lunch"] == "x"]

# Settings
chosen_meals = []
leftover_meal_1 = None
leftover_amount_1 = 0
leftover_meal_2 = None
leftover_amount_2 = 0


# Main functions

def pick_random_meal(meal_db, min_amount=0, max_amount=None, limit_selection=True):
    global chosen_meals

    if max_amount is not None:
        eligible_meals = meal_db[
            (meal_db['Amount'] >= min_amount) &
            (meal_db['Amount'] <= max_amount) &
            (~meal_db['Meal'].isin(chosen_meals))
            ]
    else:
        eligible_meals = meal_db[
            (meal_db['Amount'] >= min_amount) &
            (~meal_db['Meal'].isin(chosen_meals))
            ]

    if not eligible_meals.empty:
        random_row = eligible_meals.sample()
        random_meal = random_row.iloc[0]

        current_meal = random_meal

        if limit_selection == True:
            chosen_meals.append(current_meal[0])

        return current_meal
    else:
        current_meal = "No meal options available."
        return current_meal


def generate_meal_plan(data_lunch, data_dinner, num_days, single_lunch_days, ready_lunch_days):
    meal_plan = pd.DataFrame(index=['lunch', 'dinner'])

    global meals_left
    global leftover_meal_1
    global leftover_amount_1
    global leftover_meal_2
    global leftover_amount_2

    meal_placeholder = None

    # Saves requirements for next lunch
    next_lunch_ready = False
    next_lunch_single = False

    for day in range(1, num_days + 1):

        lunch_choice, dinner_choice = None, None

        # Check next lunch for single or ready made requirement
        if day + 1 in ready_lunch_days:
            next_lunch_ready = True
        else:
            next_lunch_ready = False

        if day in single_lunch_days:
            next_lunch_single = True
        else:
            next_lunch_single = False

        # CHECK LEFTOVER STATE (move forward form 2 if 1 empty)
        if leftover_amount_1 <= 0 and leftover_amount_2 != 0:
            leftover_meal_1 = leftover_meal_2
            leftover_amount_1 = leftover_amount_2

            leftover_meal_2 = None
            leftover_amount_2 = 0

        # LUNCH SELECTION

        # Check if there are leftovers, otherwise choose a new lunch from lunch db
        if next_lunch_single == True:
            if leftover_amount_1 == 1:
                lunch_choice = leftover_meal_1
                leftover_amount_1 -= 1

                # At this point leftovers 1 is empty, moving 2 into 1
                leftover_meal_1 = leftover_meal_2
                leftover_amount_1 = leftover_amount_2

                leftover_meal_2 = None
                leftover_amount_2 = 0

            elif leftover_amount_1 > 1:
                lunch_choice = leftover_meal_1
                leftover_amount_1 -= 1
            else:
                lunch_choice = pick_random_meal(data_lunch, min_amount=0, limit_selection=False)["Meal"]
        else:
            if leftover_amount_1 == 1:
                if leftover_amount_2 >= 1:
                    lunch_choice = f"{leftover_meal_1} + {leftover_meal_2}"
                    leftover_amount_1 -= 1
                    leftover_amount_2 -= 1

                    # At this point leftovers 1 is empty, moving 2 into 1
                    leftover_meal_1 = leftover_meal_2
                    leftover_amount_1 = leftover_amount_2

                    leftover_meal_2 = None
                    leftover_amount_2 = 0
                else:
                    lunch_choice = f"{leftover_meal_1} + something"
                    leftover_amount_1 -= 1

            elif leftover_amount_1 == 2:
                lunch_choice = leftover_meal_1
                leftover_amount_1 -= 2

                # At this point leftovers 1 is empty, moving 2 into 1
                leftover_meal_1 = leftover_meal_2
                leftover_amount_1 = leftover_amount_2

                leftover_meal_2 = None
                leftover_amount_2 = 0

            elif leftover_amount_1 > 2:
                lunch_choice = leftover_meal_1
                leftover_amount_1 -= 2
            else:
                lunch_choice = pick_random_meal(data_lunch, min_amount=0, limit_selection=False)["Meal"]

        # DINNER SELECTION

        # In case not ready and not single lunch, pick dinner
        if next_lunch_ready == False:
            if leftover_amount_1 + leftover_amount_2 >= 2:
                meal_placeholder = pick_random_meal(data_dinner, min_amount=0, max_amount=2, limit_selection=True)
                dinner_choice = meal_placeholder["Meal"]
                meals_left = meal_placeholder["Amount"]

                meals_left -= 2

            else:
                meal_placeholder = pick_random_meal(data_dinner, min_amount=0, limit_selection=True)
                dinner_choice = meal_placeholder["Meal"]
                meals_left = meal_placeholder["Amount"]

                meals_left -= 2
        elif next_lunch_ready == True:
            if leftover_amount_1 + leftover_amount_2 < 2:
                meal_placeholder = pick_random_meal(data_dinner, min_amount=4, limit_selection=True)
                dinner_choice = meal_placeholder["Meal"]
                meals_left = meal_placeholder["Amount"]

                meals_left -= 2
            else:
                meal_placeholder = pick_random_meal(data_dinner, min_amount=0, limit_selection=True)
                dinner_choice = meal_placeholder["Meal"]
                meals_left = meal_placeholder["Amount"]

                meals_left -= 2

        # Update the meal plan
        meal_plan.at['lunch', day] = lunch_choice
        meal_plan.at['dinner', day] = dinner_choice

        # At the end of day, check dinner leftovers and move to leftover variables
        if meals_left > 0:
            leftover_meal_2 = dinner_choice
            leftover_amount_2 = meals_left

            meals_left = 0

    return meal_plan


# Ingredients functionality
def get_ingredients():
    ingredients_str = data_dinner["Ingredients"][0]
    ingredients_list = re.findall(r'(\w+)\s*=\s*(\d+)', ingredients_str)
    total_ingredients = {}

    for meal in chosen_meals:
        # Get the row where the Meal column matches the current chosen meal
        row = data_dinner[data_dinner["Meal"] == meal]

        if not row.empty:
            # Get the ingredients string for the current meal
            ingredients_str = row["Ingredients"].values[0]

            # Check if the value is a valid string (not NaN)
            if pd.notna(ingredients_str):
                # Using regular expression to find key-value pairs in the string
                matches = re.findall(r'(\w+)\s*=\s*(\d+)', ingredients_str)

                # Extracting individual ingredients
                for match in matches:
                    ingredient, quantity = match

                    # Accumulate total quantity for each ingredient
                    if ingredient in total_ingredients:
                        total_ingredients[ingredient] += int(quantity)
                    else:
                        total_ingredients[ingredient] = int(quantity)

    # Output total ingredients
    ingredient_df = pd.DataFrame(total_ingredients.items(), columns=['Ingredient', 'Total Quantity'])

    return ingredient_df
