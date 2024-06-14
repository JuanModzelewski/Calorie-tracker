# Libraries
from os import system, name
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
MENU_HEADING_STYLE = Fore.WHITE + "▌│█║▌║▌║▌│█║▌║▌║"
THREE_SPACE = " " * 3
FIVE_SPACE = " " * 5
EIGHT_SPACE = " " * 8
TWELVE_SPACE = " " * 12
SIXTEEN_SPACE = " " * 16
TITLE = ""

class DataType:
    TWO_MENU_ITEMS = "two_menu_items"
    THREE_MENU_ITEMS = "three_menu_items"
    FOUR_MENU_ITEMS = "four_menu_items"
    FIVE_MENU_ITEMS ="five_menu_items"
    INTEGER = "integer"
    ENTRY_NAME = "item_name"

# ASCII art generator: https://manytools.org/hacker-tools/ascii-banner/
def welcome_screen():
    """
    Displays Banner and welcome message
    """
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
        loadingMenu(f"{EIGHT_SPACE} LOADING CALORIE TRACKER, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
        pause_and_clear()
        calorie_tracker_menu()

# Concept and tutorial used from https://www.101computing.net/python-typing-text-effect/
def loadingMenu(text, text_color = Fore.BLACK, background_color = Back.WHITE):
    for character in text:
        sys.stdout.write(text_color + background_color + character)
        sys.stdout.flush()
        time.sleep(0.01)

def typingPrint(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.02)

def pause_and_clear():
    """
    Clears screen after a brief pause.
    """
    time.sleep(1.5)
    clear_screen()

def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

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
    view_calorie_tracker = calorie_tracker.get_all_values()
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
    print(THREE_SPACE + Fore.GREEN + f"CURRENT CALORIE GOAL: {round(view_calorie_goal, 2)}")
    print(THREE_SPACE + Fore.YELLOW + f"REMAINING CALORIES: {round(remaining_calories, 2)}")
    print()
    print(Fore.BLUE + "CURRENTLY TRACKED ITEMS:")
    print(tabulate(view_calorie_tracker, tablefmt="rounded_grid",maxcolwidths=[10, 9, 25, 8, 8]))
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
            loadingMenu(f"{EIGHT_SPACE} LOADING CALORIE GOAL, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            pause_and_clear()
            sys.stdout.flush()
            update_calorie_goal()
            break

        elif user_input =="2":
            #TITLE = THREE_SPACE + Fore.BLUE + "NEW ITEM MENU" + THREE_SPACE
            print()
            loadingMenu(f"{EIGHT_SPACE} PREPARING NEW ITEM, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            pause_and_clear()
            sys.stdout.flush()
            add_food_item()
            break

        elif user_input == "3":
            #TITLE = THREE_SPACE + Fore.BLUE + "SEARCH FOOD LIBRARY" + THREE_SPACE
            print()
            loadingMenu(f"{EIGHT_SPACE} PREPARING TO SEARCH, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            pause_and_clear()
            sys.stdout.flush()
            search_food_library()
            break
        
        elif user_input == "4":
            #TITLE = THREE_SPACE + Fore.BLUE + "REMOVE ITEMS FROM TRACKER" + THREE_SPACE
            print()
            loadingMenu(f"{EIGHT_SPACE} LOADING ITEMS, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            pause_and_clear()
            sys.stdout.flush()
            remove_tracked_item()
            break
        

# Manually add Food Items / Calorie Tracker Menu
def add_food_item():
    """
    Manually adds food item by creating an list entry from each function using user input.
    The final list item is confirmed, the user is able to add list item to tracker and to library.
    """
    new_entry = []
    date = datetime.now()
    date_entry = date.strftime("%d-%m-%Y")
    new_entry.insert(0,date_entry)
    item_table = []
    item_table.append(new_entry)
    headers = ["Date", "Meal", "Name", "kCal per 100g", "Serving Size (g)"]

    # Confirm Item Information, add to Tracker and Library
    def item_confirmation():
        """
        new_entry list is tabulated and displayed as a preview
        Calculation for item calories is done by dividing calories per 100g by 100 and multiplying by serving size
        The user is given options to add item to tracker or add item to library
        If Add item to Tracker is selected the required indexes are taken from new_entry list and added to calorie_tracker sheet
        If Save Item to library is selected the required indexes are taken from new_entry list and added to food_library sheet

        """
        print()
        print(THREE_SPACE + "ENTRY PREVIEW", Fore.BLUE)
        print(tabulate(item_table, headers, tablefmt="rounded_grid",maxcolwidths=[None, None, 25, 8, 8]))
        print()

        # Serving Calories
        item_total_calories = [(float(new_entry[3]) / 100) * float(new_entry[4])]

        typingPrint(THREE_SPACE + "Please select one of the following options:\n")
        print()

        for idx, menu_item in enumerate(ITEM_CONFIRMATION_SELECTION):
            print(FIVE_SPACE + str(idx + 1) + ". " + menu_item)
        print()

        while True:

            user_input = input("    > ")

            if user_input == "1":
                date_meal_name = slice(0,3)
                serving_size = slice(4,5)
                calorie_tracker.append_row(new_entry[date_meal_name] + new_entry[serving_size]  + item_total_calories)
                print()
                loadingMenu(f"{EIGHT_SPACE} ADDING ITEM TO TRACKER, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
                pause_and_clear()
                calorie_tracker_menu()
                break

            elif user_input == "2":
                food_library.append_row(new_entry[2:4])
                print()
                loadingMenu(f"{EIGHT_SPACE} ADDING ITEM TO LIBRARY, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
                print()
                pause_and_clear()
                item_confirmation()
                break

            elif user_input == "3":
                calorie_tracker_menu()
                break
                
            else:
                validate_data(DataType.THREE_MENU_ITEMS, user_input)

    # Add Serving Size to list
    def item_serving():
        """
        Validates user input to ensure that only numbers are entered
        If valid the entry is added to new_entry list
        """
        while True:
            print()
            typingPrint(THREE_SPACE + "Enter your serving size in grams:\n")
            print()

            user_input = input("    > ")

            if validate_data(DataType.INTEGER, user_input): 
                new_entry.append(int(user_input))
                pause_and_clear()
                item_confirmation()
                break
    
    # Add Item Calories per 100g to list            
    def item_calories():
        """
        Validates user input to ensure that only numbers are entered
        If valid the entry is added to new_entry list
        """
        while True:
            print()
            typingPrint(THREE_SPACE + "Enter the amount of Calories(kCal) per 100g\n")
            print(THREE_SPACE + "**NOTE You can get this information from the nutritional label at the back of the product\n")
            print()

            user_input = input("    > ")

            if validate_data(DataType.INTEGER, user_input): 
                new_entry.append(int(user_input))
                item_serving()
                break
      
    # Add Item Name to list 
    def item_name():
        """
        The users input is validated to ensure the entry is no blank and no more than 50 character
        If the entry is valid the entry is added to the new_entry list
        """
        while True:
            print()
            typingPrint(THREE_SPACE + "Please provide a Name for your food item\n")
            print(THREE_SPACE +  "eg Crumb Chicken 'BRAND NAME'\n")
            print()

            user_input = input("    > ")

            if validate_data(DataType.ENTRY_NAME, user_input): 
                new_entry.append(user_input.capitalize())
                item_calories()
                break
 
    # Add meal to list
    def item_meal():
        """
        Validates user input to ensure only available options are entered
        Add the selected entry to the new_entry list
        """
        while True:
            print()
            typingPrint(THREE_SPACE + "Please select one of the following options:\n")
            print()

            for idx, meal in enumerate(MEAL_TYPES):
              print(FIVE_SPACE + str(idx + 1) + ". " + meal)
            print()

            user_input = input("    > ")

            if user_input in ["1", "2", "3", "4"]:
              new_entry.insert(1, MEAL_TYPES[int(user_input) - 1])
              pause_and_clear()
              item_name()
              break
            
            else:
                validate_data(DataType.FOUR_MENU_ITEMS, user_input)


    item_meal()   

# Search food library and add food items to Tracker / Calorie Tracker Menu
def search_food_library():
    """
    Holds all functions that allow user to search library and add item to tracker
    """
    # Item added to Tracker
    def add_search_item():
        """
        Current date added to list
        Calculation for item calories is done by dividing calories per 100g by 100 and multiplying by serving size
        The calculation is added to the list and the calories per 100g is removed
        The final list is added to the calorie tracker sheet
        """
        # Date item added to list
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
        search_food_library()

    # Serving size for item
    def search_serving():
        """
        Validates user input to ensure input is a number
        Adds the serving size to the list
        """
        while True:
            print()
            typingPrint(THREE_SPACE + "Enter your serving size in grams:\n")
            print()

            user_input = input("    > ")

            if validate_data(DataType.INTEGER, user_input):
                selected_flat_list.append(int(user_input))
                add_search_item()
                print()
                loadingMenu(f"{EIGHT_SPACE} ADDING ITEM TO TRACKER, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
                time.sleep(0.5)
                pause_and_clear()
                calorie_tracker_menu()
                break

    # Meal option for item                
    def search_meal():
        """
        Adds meal item to list which, displayed in final Tracker table
        Available options are presented and chosen option added to the list
        """
        while True:
            print()
            typingPrint("   Please select one of the following options:\n")
            print()

            for idx, meal in enumerate(MEAL_TYPES):
              print(FIVE_SPACE + str(idx+1) + ". " + meal)
            print()

            user_input = input("    > ")

            if user_input in ["1", "2", "3", "4"]:
              selected_flat_list.insert(0, MEAL_TYPES[int(user_input) - 1])
              search_serving()
              pause_and_clear()
              break
            
            else:
                validate_data(DataType.FOUR_MENU_ITEMS, user_input)

    # Confirmation of selected item
    def confirm_selected_item():
        """
        Displays the selected item for confirmation
        Provides options to add item, proceeding to next step or return to search
        """
        print()
        print(THREE_SPACE + Fore.BLUE + "YOUR SELECTION:")
        headers = ["Food Item", "kCal per 100g"]
        print(tabulate(selected_item, headers, tablefmt="rounded_grid",maxcolwidths=[30,10]))
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
                search_meal()
                break
            
            elif user_input == "2": 
                pause_and_clear()
                search_food_library() 
                break

            else: 
                validate_data(DataType.TWO_MENU_ITEMS, user_input)
            
    # Select Food Item from search_item_list
    def select_food_item():
        """
        Validates user input to ensure that it is a number
        Fetches the item from corresponding index and input
        If there is no item in the index position an error message is displayed
        """
        print()
        typingPrint(THREE_SPACE + "Select a number from the first colum to add food item:\n")
        print()

        global selected_item
        selected_item = []

        while True:

            user_input = int(input("    > "))

            try:
                if user_input == 0:
                    raise ValueError("Heading cannot be selected\n")

                for i in search_item_list:
                    if user_input == search_item_list.index(i):
                        selected_item.append(search_item_list[user_input])
                        pause_and_clear()
                        confirm_selected_item()
                        break

                for i in search_item_list:
                    if user_input != search_item_list.index(i): 
                        raise ValueError("Select a number from the first colum\n")
                    
            except ValueError as e:
                print()
                print(Fore.RED + THREE_SPACE + f"Invalid data: {e}\n")

    # Main Search Function searches food item sheet for user input
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
        typingPrint(THREE_SPACE + "Please type the food item you are looking for:\n")
        print()
        print(THREE_SPACE + "Type 'exit' to return to the Calorie Tracker menu")
        print()

        while True:
            
            user_input = input("    > ")

            # Find all instances of user input in sheet
            if validate_data("search_food_library", user_input): 
                search_items = re.compile(user_input.capitalize())
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
                    global search_item_list
                    search_item_list = []

                    # Removes duplicates from list
                    [search_item_list.append(x) for x in search_items if x not in search_item_list]

                    search_headers = ["Food Item", "kCal per 100g"]
                    search_item_list.insert(0, search_headers)
                    search_table = tabulate(search_item_list, tablefmt="rounded_grid", showindex="always", maxcolwidths=[None, 30, 10])
                    pause_and_clear()
                    print(THREE_SPACE + Fore.BLUE + "AVAILABLE OPTIONS:")
                    print(search_table)
                    select_food_item()
            
            validate_food_search()
            
            return False

    search_main()

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
    print(THREE_SPACE + Fore.BLUE + "CURRENTLY TRACKED ITEMS:")
    print(tabulate(view_calorie_tracker, tablefmt="rounded_grid",showindex="always", maxcolwidths=[5, 10, 9, 25, 8, 8]))
    print()
    typingPrint(THREE_SPACE + "Select a number from the first colum to remove food item:\n")
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
                    loadingMenu(f"{EIGHT_SPACE} REMOVING ITEM, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.BLACK, Back.WHITE)
                    print()
                    remove_tracked_item()
                    break

            for i in view_calorie_tracker:
                if int(user_input) != view_calorie_tracker.index(i):
                    raise ValueError("Select a number from the first colum\n")
                break
                
        except ValueError as e:
            print()
            print(Fore.RED + THREE_SPACE + f"Invalid data: {e}\n")

def menu_input_validation(value, max_value):
  possible_values = [str(i+1) for i in range(max_value)]
  if value not in possible_values:
    raise ValueError("Select option 1 to " + str(max_value))

# Input Validation
def validate_data(data, value):
    """
    Validates user input throughout program
    """
    try:       
        # Validates input for two menu items
        if data == DataType.TWO_MENU_ITEMS:
            menu_input_validation(value, 2)

        # Validates input for three menu
        elif data == DataType.THREE_MENU_ITEMS:
            menu_input_validation(value, 3)
            
        # Validates input for four menu    
        elif data == DataType.FOUR_MENU_ITEMS:
            menu_input_validation(value, 4)
            
        # Validates input for five menu    
        elif data == DataType.FIVE_MENU_ITEMS:
            menu_input_validation(value, 5)
        
        # Update Calorie Data Validation 
        elif data == "calorie_data":    
            if not 1500 <= int(value) <= 3500:
                raise ValueError("Select a goal between 1500 and 3500")
        
        elif data == DataType.INTEGER:
            if not int(value):
                raise ValueError("You can only enter numbers")
               
        # Validates string length for item added to tracker and library    
        elif data == DataType.ENTRY_NAME:
            if not value != "" or len(value) > 50 :
                raise ValueError("Category must be between 0 and 50 characters") 

        # Search criteria must be 3 characters or more
        elif data == "search_food_library":
            if len(value) < 3:
                raise ValueError("A minimum of 3 characters required")
            
    except ValueError as e:
            print()
            print(Fore.RED + THREE_SPACE + f"Invalid data: {e}\n")
            return False
         
    return True

# Update Calorie Goal / Calories Tracker Menu
def update_calorie_goal():
    """
    Allow user to set new calorie goal
    Validates user input to ensure goal is realistic between 1500 and 3500 calories
    Updated cell on Calorie Goal sheet
    """
    while True:
        print()
        typingPrint(THREE_SPACE + "Please enter your new calorie goal:\n")
        print()

        user_input = input("    > ")

        if validate_data("calorie_data", user_input):
            print()
            loadingMenu(f"{FIVE_SPACE} UPDATING CALORIE GOAL, PLEASE WAIT {FIVE_SPACE}".center(70), Fore.BLACK, Back.WHITE)
            calorie_goal.update_cell(2,2, user_input)
            pause_and_clear()
            calorie_tracker_menu()

            if validate_data(DataType.INTEGER, user_input): update_calorie_goal()
            break
                


welcome_screen()