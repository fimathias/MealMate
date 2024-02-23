from gui import display_meal_plan_info
from meal_plan_generator import regenerate_meal_plan

if __name__ == "__main__":
    # Call the display_meal_plan_info function directly
    meals = regenerate_meal_plan()[0]
    ingredients = regenerate_meal_plan()[1]
    display_meal_plan_info(meals, ingredients)
