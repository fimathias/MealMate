from data import generate_meal_plan, data_DB, get_ingredients
import pandas as pd

# Settings
num_days = 8  # Number of days to generate
single_lunch_days = []  # Which days only require 1 lunch
ready_lunch_days = [3, 4, 5, 6, 7]  # Which days require lunch to be leftovers from previous days

# Subset of list
data_dinner = data_DB[pd.isnull(data_DB["Lunch"])]
data_lunch = data_DB[data_DB["Lunch"] == "x"]


def regenerate_meal_plan():
    meal_plan_result = generate_meal_plan(data_lunch, data_dinner, num_days, single_lunch_days, ready_lunch_days)
    ingredients = get_ingredients()
    return meal_plan_result, ingredients
