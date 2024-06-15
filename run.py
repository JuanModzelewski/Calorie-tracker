# Libraries
import os
import sys
import time

import colorama
import gspread
import re

from datetime import datetime

from collections import defaultdict
from colorama import Back, Fore, Style
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from utilities import loading_menu, typing_print, pause_and_clear, DATA_TYPE, validate_data


# Initialize colorama for text formatting https://linuxhint.com/colorama-python/
colorama.init(autoreset=True)

# Scope for Google IAM for API access 
# Tutorial from Code Institute Love Sandwiches Essential Project
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


# Variables to access spreadsheet Code Institute Love Sandwiches
# Tutorial from Code Institute Love Sandwiches Essential Project
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("calorie_tracker")


#GSPREAD SHEETS
calorie_tracker = SHEET.worksheet("calorie_tracker")
calorie_goal = SHEET.worksheet("calorie_goal")
weight_tracker = SHEET.worksheet("weight_tracker")
food_library = SHEET.worksheet("food_items")


ITEM_CONFIRMATION_SELECTION = ["Add Item to Tracker", "Save Item to library", "Back to Calorie Tracker"]
SEARCH_CONFIRMATION_SELECTION = ["Add Item to Tracker", "Back to Search"]
MEAL_TYPES =  ["Breakfast", "Lunch", "Dinner", "Snack"]
MENU_HEADING_STYLE = Fore.WHITE + "----------------"
THREE_SPACE = " " * 3
FIVE_SPACE = " " * 5
EIGHT_SPACE = " " * 8
TWELVE_SPACE = " " * 12
SIXTEEN_SPACE = " " * 16
TITLE = ""

global new_entry
new_entry = []

global date
date = datetime.now()

global date_entry
date_entry = date.strftime("%d-%m-%Y")

global search_item_list
search_item_list = []

# ASCII art generator: https://manytools.org/hacker-tools/ascii-banner/
def welcome_screen():
    """
    Displays Banner and welcome message
    """
    print(Fore.BLUE + r'''
        ██████╗ █████╗ ██╗      ██████╗ ██████╗ ██╗███████╗     
        ██╔════╝██╔══██╗██║     ██╔═══██╗██╔══██╗██║██╔════╝     
        ██║     ███████║██║     ██║   ██║██████╔╝██║█████╗       
        ██║     ██╔══██║██║     ██║   ██║██╔══██╗██║██╔══╝       
        ╚██████╗██║  ██║███████╗╚██████╔╝██║  ██║██║███████╗     
        ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝     
                                                                    
      ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
      ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
         ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
         ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
         ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
         ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                                                               
    ''')
    print(Fore.BLUE + "WELCOME TO CALORIE TRACKER".center(70))
    print("Your daily calorie tracking tool to ensure you meet your".center(70))
    print("calorie requirements and achieve you goals.\n".center(70))
    print(Fore.BLUE + "GETTING STARTED".center(70))
    print("Set your calorie goal in the calorie tracker menu.".center(70))
    print("Manually add an entry or search the Food Library.".center(70))
    print("Items can be added to Food Library by Manually adding".center(70))
    print("an item and choosing to save to library.".center(70))
    print()
    user_input = input(Fore.GREEN + "PRESS ENTER TO CONTINUE".center(70))
    time.sleep(0.5)

    if user_input == "":
        print()
        loading_menu(f"{EIGHT_SPACE} LOADING CALORIE TRACKER, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
        pause_and_clear()
        calorie_tracker_menu()

def tracker_table(menu):
    
    date = datetime.now()
    current_date = date.strftime("%d-%m-%Y")
    search_entries = re.compile(current_date)
    tracker_date = calorie_tracker.findall(search_entries)
    tracker_entries = []
    tracker_headers = ["\nMeal", "\nFood Item", "Serving\nSize (g)", "\nCalories"]
    row_id = []

    for x in tracker_date:
        item = x._row
        item_row = calorie_tracker.row_values(item)
        tracker_entries.append(item_row)

    for i in tracker_entries:
        row_id.append(tracker_entries.index(i)+1)

    for x in tracker_entries:
        del x[0]
    
    if menu == "tracker_menu": 
        print(tabulate(tracker_entries, tracker_headers, tablefmt="rst", maxcolwidths=[10, 35, 7, 7], colalign=("left", "left", "center", "center")))

    elif menu == "remove_items_menu":
        print(tabulate(tracker_entries, tracker_headers, tablefmt="rst", maxcolwidths=[5, 10, 35, 7, 7], colalign=("center", "left", "left", "center", "center"), showindex = row_id))



# Calorie Tracker Menu
def calorie_tracker_menu():
    """
    Users are given options to:
    Change the calorie goal
    Manually add a new item by following steps to create a new entry
    Search and add items from food library
    Remove Tracked items
    Return to the main menu
    Validates user input and provides feedback if input is invalid
    """
    TITLE = THREE_SPACE + Fore.BLUE + "CALORIE TRACKER MENU" + THREE_SPACE
    CALORIE_TRACKER_MENU = ["Update Calorie Goal", "Manually Add Food Item", "Search & Add From Library", "Remove Item From Tracker"]

    view_calorie_goal = calorie_goal.cell(2,2, value_render_option='FORMULA').value
    calorie_values = calorie_tracker.col_values(5)
    
    # Removes heading from colum
    del calorie_values[0]

    total_calories = 0
    
    # Calculation for all sum of Calorie colum
    for x in range(0, len(calorie_values)):
        total_calories = total_calories + float(calorie_values[x])

    # Calculation for remaining Calories
    remaining_calories = view_calorie_goal - total_calories

    print()
    # Heading styles from https://textkool.com
    print(f"{MENU_HEADING_STYLE}{TITLE}{MENU_HEADING_STYLE}".center(70))
    print()
    print(Fore.BLUE + f"CURRENTLY TRACKED ITEMS: {date_entry}")
    print()
    tracker_table("tracker_menu")
    print()
    print(Fore.GREEN + f"CURRENT CALORIE GOAL: {round(view_calorie_goal, 2)}" + EIGHT_SPACE + Fore.YELLOW + f"REMAINING CALORIES: {round(remaining_calories, 2)}")
    print()
    print(THREE_SPACE + "Select one of following options:")
    print()

    for idx, menu_item in enumerate(CALORIE_TRACKER_MENU):
        print(FIVE_SPACE + str(idx + 1) + ". " + menu_item)
    print()
    
    # Loop repeats until valid input is received
    while True:

        user_input = input("    > ")

        if user_input == "1":
            #TITLE = THREE_SPACE + "CALORIE GOAL MENU" + THREE_SPACE, Fore.BLUE
            print()
            loading_menu(f"{EIGHT_SPACE} LOADING CALORIE GOAL, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            pause_and_clear()
            update_calorie_goal()
            break

        elif user_input =="2":
            #TITLE = THREE_SPACE + Fore.BLUE + "NEW ITEM MENU" + THREE_SPACE
            print()
            loading_menu(f"{EIGHT_SPACE} PREPARING NEW ITEM, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            pause_and_clear()
            entry_meal("manual_entry")
            break

        elif user_input == "3":
            #TITLE = THREE_SPACE + Fore.BLUE + "SEARCH FOOD LIBRARY" + THREE_SPACE
            print()
            loading_menu(f"{EIGHT_SPACE} PREPARING TO SEARCH, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            pause_and_clear()
            search_main()
            break
        
        elif user_input == "4":
            #TITLE = THREE_SPACE + Fore.BLUE + "REMOVE ITEMS FROM TRACKER" + THREE_SPACE
            print()
            loading_menu(f"{EIGHT_SPACE} LOADING ITEMS, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            pause_and_clear()
            remove_tracked_item()
            break


def entry_meal(method):
    """
     Validates user input to ensure only available options are entered
    Add the selected entry to the new_entry list
    """
    while True:
        print()
        typing_print(THREE_SPACE + "Please select one of the following options:\n")
        print()

        for idx, meal in enumerate(MEAL_TYPES):
            print(FIVE_SPACE + str(idx + 1) + ". " + meal)
        print()

        user_input = input("    > ")

        if user_input in ["1", "2", "3", "4"] and method == "search_entry":
            selected_flat_list.insert(0, MEAL_TYPES[int(user_input) - 1])
            entry_serving("search_entry")
            #pause_and_clear()
            break

        elif user_input in ["1", "2", "3", "4"] and method == "manual_entry":
            new_entry.insert(1, MEAL_TYPES[int(user_input) - 1])
            #pause_and_clear()
            name_manual_item()
            break
            
        else:
            validate_data(DATA_TYPE.FOUR_MENU_ITEMS, user_input)     

def add_item(method):
    date = datetime.now()
    date_entry = date.strftime("%d-%m-%Y")

    if method == "manual_entry":
        item_total_calories = [(float(new_entry[2]) / 100) * float(new_entry[3])]
        new_entry.insert(0, date_entry)
        date_meal_name = slice(0,3)
        serving_size = slice(4,5)
        calorie_tracker.append_row(new_entry[date_meal_name] + new_entry[serving_size]  + item_total_calories)

    elif method == "search_entry":
        date = datetime.now()
        date_entry = date.strftime("%d-%m-%Y")
        selected_flat_list.insert(0, date_entry)

        # Calculation for total calories-
        total_item_calories = (float(selected_flat_list[3]) / 100) * float(selected_flat_list[4])
        selected_flat_list.append(total_item_calories)
        del selected_flat_list[3]

        # Item added to calorie tracker sheet
        calorie_tracker.append_row(selected_flat_list)
        pause_and_clear()
        search_main()

def entry_serving(method):
    """
    Validates user input to ensure input is a number
    Adds the serving size to the list
    """
    while True:
        print()
        typing_print(THREE_SPACE + "Enter your serving size in grams:\n")
        print()

        user_input = input("    > ")

        if validate_data(DATA_TYPE.INTEGER, user_input) and method == "search_entry":
            selected_flat_list.append(int(user_input))
            add_item("search_entry")
            print()
            loading_menu(f"{EIGHT_SPACE} ADDING ITEM TO TRACKER, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            time.sleep(0.5)
            pause_and_clear()
            calorie_tracker_menu()
            break

        elif validate_data(DATA_TYPE.INTEGER, user_input) and method == "manual_entry":
            new_entry.append(int(user_input))
            pause_and_clear()
            calories_manual_item()
            break


# Confirm Item Information, add to Tracker and Library
def confirm_manual_item():
    """
    new_entry list is tabulated and displayed as a preview
    Calculation for item calories is done by dividing calories per 100g by 100 and multiplying by serving size
    The user is given options to add item to tracker or add item to library
    If Add item to Tracker is selected the required indexes are taken from new_entry list and added to calorie_tracker sheet
    If Save Item to library is selected the required indexes are taken from new_entry list and added to food_library sheet

    """
    # Table displaying item to be added
    item_table = []
    item_table.append(new_entry)
    headers = ["\nMeal", "\nName", "kCal\nper 100g", "Serving\nSize (g)"]

    print()
    print(THREE_SPACE + "ENTRY PREVIEW", Fore.BLUE)
    print(tabulate(item_table, headers, tablefmt="rst", maxcolwidths=[10, 35, 7, 7], colalign=("left", "left", "center", "center")))
    print()

    # Serving Calories
    typing_print(THREE_SPACE + "Please select one of the following options:\n")
    print()

    # Prints menu items
    for idx, menu_item in enumerate(ITEM_CONFIRMATION_SELECTION):
            print(FIVE_SPACE + str(idx + 1) + ". " + menu_item)
    print()

    while True:

        user_input = input("    > ")

        if user_input == "1":
            add_item("manual_entry")
            print()
            loading_menu(f"{EIGHT_SPACE} ADDING ITEM TO TRACKER, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            pause_and_clear()
            calorie_tracker_menu()
            break

        elif user_input == "2":
            food_library.append_row(new_entry[2:4])
            print()
            loading_menu(f"{EIGHT_SPACE} ADDING ITEM TO LIBRARY, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            print()
            pause_and_clear()
            confirm_manual_item()
            break

        elif user_input == "3":
            calorie_tracker_menu()
            break
                
        else:
            validate_data(DATA_TYPE.THREE_MENU_ITEMS, user_input)
    
# Add Item Calories per 100g to list            
def calories_manual_item():
    """
    Validates user input to ensure that only numbers are entered
    If valid the entry is added to new_entry list
    """
    while True:
        print()
        typing_print(THREE_SPACE + "Enter the amount of Calories(kCal) per 100g\n")
        print(THREE_SPACE + "**NOTE You can get this information from the nutritional label at the back of the product\n")
        print()

        user_input = input("    > ")

        if validate_data(DATA_TYPE.INTEGER, user_input): 
            new_entry.append(int(user_input))
            entry_serving("manual_entry")
            break
    
# Add Item Name to list 
def name_manual_item():
    """
    The users input is validated to ensure the entry is no blank and no more than 50 character
    If the entry is valid the entry is added to the new_entry list
    """
    while True:
        print()
        typing_print(THREE_SPACE + "Please provide a Name for your food item\n")
        print(THREE_SPACE +  "eg Crumb Chicken 'BRAND NAME'\n")
        print()

        user_input = input("    > ")

        if validate_data(DATA_TYPE.ENTRY_NAME, user_input): 
            new_entry.append(user_input.title())
            calories_manual_item()
            break


def confirm_search_item():
    """
    Displays the selected item for confirmation
    Provides options to add item, proceeding to next step or return to search
    """
    print()
    print(THREE_SPACE + Fore.BLUE + "YOUR SELECTION:")
    headers = ["\nFood Item", "kCal\nper 100g"]
    print(tabulate(selected_item, headers,  tablefmt="rst", maxcolwidths=[30, 10], colalign=("left", "center")))
    print()

    while True:

        for idx, menu_item in enumerate(SEARCH_CONFIRMATION_SELECTION):
            print(FIVE_SPACE + str(idx + 1) + ". " + menu_item)
            print()

        # flat list is created for next steps so items can be added and list can be tabulated correctly
        global selected_flat_list
        selected_flat_list = [element for innerList in selected_item for element in innerList]

        user_input = input("    > ")

        if user_input == "1": 
            pause_and_clear() 
            entry_meal("search_entry")
            break
        
        elif user_input == "2": 
            pause_and_clear()
            search_main()
            break

        else: 
            validate_data(DATA_TYPE.TWO_MENU_ITEMS, user_input)

def select_search_item():
    """
    Validates user input to ensure that it is a number
    Fetches the item from corresponding index and input
    If there is no item in the index position an error message is displayed
    """
    print()
    typing_print(THREE_SPACE + "Select a number from the first colum to add food item:\n")
    print()

    global selected_item
    selected_item = []

    while True:

        user_input = int(input("    > "))

        try:
            for i in search_item_list:
                if user_input == search_item_list.index(i) + 1:
                    selected_item.append(search_item_list[user_input - 1])
                    pause_and_clear()
                    confirm_search_item()
                    break

            for i in search_item_list:
                if user_input != search_item_list.index(i) + 1: 
                    raise ValueError("Select a number from the first colum\n")
                    
        except ValueError as e:
            print()
            print(Fore.RED + THREE_SPACE + f"Invalid data: {e}\n")

def search_main():
    """
    Takes user input, validates input to a minimum of 3 characters
    Searches food library sheet for matching items
    If an item is not found an error is displayed and search repeats.
    If item is found the item row is added to a list
    Results are tabulated and displayed
    """

    TITLE = THREE_SPACE + Fore.BLUE + "SEARCH FOOD LIBRARY" + THREE_SPACE

    print()
    # Heading styles from https://textkool.com
    print(f"{MENU_HEADING_STYLE}{TITLE}{MENU_HEADING_STYLE}".center(70))
    print()
    typing_print(THREE_SPACE + "Please type the food item you are looking for:\n")
    print()
    print(THREE_SPACE + "Type 'exit' to return to the Calorie Tracker menu")
    print()

    while True:
            
        user_input = input("    > ")

        # Find all instances of user input in sheet
        if validate_data("search_food_library", user_input): 
            search_items = re.compile(user_input.title())
            get_food_items = food_library.findall(search_items)
            
            search_items = []

            # Loop through all instances and add items row to search_items list
            for x in get_food_items:
                item = x._row
                item_row = food_library.row_values(item)
                search_items.append(item_row)
                    

            # Allows user to exit search
            if user_input == "exit":
                pause_and_clear()
                calorie_tracker_menu()
                break
            

        # Validates search_items, if item could not be found error message is displayed
        def validate_food_search():
            if len(search_items) == 0:
                print()
                print(THREE_SPACE + Fore.RED + "There are no items matching your search criteria")
                print()
                search_main()
                
            # If items are found remove possible duplicates and add to search_items_list for tabulate
            else:
                row_id = []

                # Removes duplicates from list
                [search_item_list.append(x) for x in search_items if x not in search_item_list]

                for i in search_item_list:
                    row_id.append(search_item_list.index(i)+1)

                search_headers = ["Food Item", "kCal per 100g"]
                search_table = tabulate(search_item_list, headers = search_headers, tablefmt="rst", maxcolwidths=[5, 35, 7], colalign=("center", "left", "center"), showindex = row_id)
                pause_and_clear()
                print(Fore.BLUE + "AVAILABLE OPTIONS:")
                print(search_table)
                select_search_item()
            
        validate_food_search()
            
        return False


# Removes items from Tracker
def remove_tracked_item():
    """
    Allows user to remove items from calorie tracker
    Tabulates tracker and displays item indexes
    Validates input so headings cannot be removed, 
    unavailable index input cannot be selected and only numbers can be entered
    If input is valid items from corresponding row are removed from calorie tracker sheet
    """
    global view_calorie_tracker
    view_calorie_tracker = calorie_tracker.get_all_values()

    TITLE = THREE_SPACE + Fore.BLUE + "REMOVE ITEMS MENU" + THREE_SPACE

    print(f"{MENU_HEADING_STYLE}{TITLE}{MENU_HEADING_STYLE}".center(70))
    print()
    print(Fore.BLUE + "CURRENTLY TRACKED ITEMS:")
    tracker_table("remove_items_menu")
    print()
    typing_print(THREE_SPACE + "Select a number from the first colum to remove food item:\n")
    print()
    print(THREE_SPACE + Fore.LIGHTWHITE_EX + "Type 'exit to return to Calorie Tracker'\n")

    while True:
        
        user_input = input("    > ")

        if user_input == "exit":
            pause_and_clear()
            sys.stdout.flush()
            calorie_tracker_menu()
            break

        try:
            if user_input == "0":
                raise ValueError("Headings can not be removed\n")

            for i in view_calorie_tracker:
                if int(user_input) == view_calorie_tracker.index(i):
                    calorie_tracker.delete_rows(int(user_input)+1)
                    print()
                    loading_menu(f"{EIGHT_SPACE} REMOVING ITEM, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
                    print()
                    pause_and_clear()
                    remove_tracked_item()
                    break

            for i in view_calorie_tracker:
                if int(user_input) != view_calorie_tracker.index(i):
                    raise ValueError("Select a number from the first colum\n")
                break
                
        except ValueError as e:
            print()
            print(Fore.RED + THREE_SPACE + f"Invalid data: {e}\n")


# Update Calorie Goal / Calories Tracker Menu
def update_calorie_goal():
    """
    Allow user to set new calorie goal
    Validates user input to ensure goal is realistic between 1500 and 3500 calories
    Updated cell on Calorie Goal sheet
    """
    while True:
        print()
        typing_print(THREE_SPACE + "Please enter your new calorie goal:\n")
        print()

        user_input = input("    > ")

        if validate_data("calorie_data", user_input):
            print()
            loading_menu(f"{FIVE_SPACE} UPDATING CALORIE GOAL, PLEASE WAIT {FIVE_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            calorie_goal.update_cell(2,2, user_input)
            pause_and_clear()
            calorie_tracker_menu()

            if validate_data(DATA_TYPE.INTEGER, user_input): update_calorie_goal()
            break

def main():
    welcome_screen()

main()