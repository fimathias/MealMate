import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import Button
import pandas as pd


def display_meal_plan_info(meal_plan_df, ingredient_df):
    # Set pandas display options to show all columns and rows
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # Create a new window
    window = tk.Tk()

    # Set the window settings
    window.title("Meal Plan Program")
    window.geometry("1400x750")

    # Create a scrolled text widget to display the meal plan info
    text_widget = ScrolledText(window, wrap=tk.WORD)
    text_widget.pack(expand=True, fill='both')

    # Convert meal df to string and display in the scrolled text widget
    meal_plan_string = meal_plan_df.to_string(index=False)  # Convert DataFrame to string
    text_widget.insert(tk.END, meal_plan_string)

    # Convert ingredient df to string and display in the scrolled text widget
    ingredient_string = ingredient_df.to_string(index=False)  # Convert DataFrame to string
    text_widget.insert(tk.END, '\n\n')
    text_widget.insert(tk.END, ingredient_string)
    text_widget.configure(state='disabled')  # Make the text widget read-only

    # Add a button to regenerate meal plan
    regenerate_button = Button(window, text="Exit", command=window.destroy)
    regenerate_button.pack()

    tk.mainloop()
