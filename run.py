# Libraries
import os
import sys
import time

import colorama
import gspread
import re

import datetime

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



# ASCII art generator: https://manytools.org/hacker-tools/ascii-banner/
def welcome_screen():
    """
    Displays Banner and welcome message
    """
    # Logo
    print(Fore.BLUE + r'''                                                                                                                                                                                                                                             
              ,ad8888ba,         db         88           ,ad8888ba,    88888888ba   88  88888888888           
             d8"'    `"8b       d88b        88          d8"'    `"8b   88      "8b  88  88                    
            d8'                d8'`8b       88         d8'        `8b  88      ,8P  88  88                    
            88                d8'  `8b      88         88          88  88aaaaaa8P'  88  88aaaaa               
            88               d8YaaaaY8b     88         88          88  88""""88'    88  88"""""               
            Y8,             d8""""""""8b    88         Y8,        ,8P  88    `8b    88  88                    
             Y8a.    .a8P  d8'        `8b   88          Y8a.    .a8P   88     `8b   88  88                    
              `"Y8888Y"'  d8'          `8b  88888888888  `"Y8888Y"'    88      `8b  88  88888888888           
                                                                                                                                                                                                                                                                                                                   
       888888888888  88888888ba          db         ,ad8888ba,   88      a8P   88888888888  88888888ba   
            88       88      "8b        d88b       d8"'    `"8b  88    ,88'    88           88      "8b  
            88       88      ,8P       d8'`8b     d8'            88  ,88"      88           88      ,8P  
            88       88aaaaaa8P'      d8'  `8b    88             88,d88'       88aaaaa      88aaaaaa8P'  
            88       88""""88'       d8YaaaaY8b   88             8888"88,      88"""""      88""""88'    
            88       88    `8b      d8""""""""8b  Y8,            88P   Y8b     88           88    `8b    
            88       88     `8b    d8'        `8b  Y8a.    .a8P  88     "88,   88           88     `8b   
            88       88      `8b  d8'          `8b  `"Y8888Y"'   88       Y8b  88888888888  88      `8b                                                                                                                                                                                                                                                                                                                               
    ''')

    print(Fore.BLUE + "         WELCOME TO CALORIE TRACKER")
    print("     Your daily calorie tracking tool to ensure you meet your")
    print("         calorie requirements and achieve you goals.\n")
    print(Fore.BLUE + "         GETTING STARTED")
    print("     Set your calorie goal in the calorie tracker menu.")
    print("     Manually add an entry or search the Food Library.")
    print("     Items can be added to Food Library by Manually adding")
    print("         an item and choosing to save to library.")
    print()
    user_input = input(Fore.GREEN + "PRESS ENTER TO CONTINUE")
    time.sleep(0.5)

    if user_input == "":
        print()
        loadingMenu("           LOADING MAIN MENU, PLEASE WAIT...           ", Fore.BLACK, Back.WHITE)
        clearScreen()
        main_menu()

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

def typingInput(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.02)
  value = input()  
  return value

def clearScreen():
  os.system('cls' if os.name == 'nt' else 'clear')

def menu_navigation():
    main_menu()
    
# Main Menu
def main_menu():
    """
    Runs the main menu of the program.
    Allows users to navigate through program.
    Validates user input and provides feedback if input is invalid
    """
    print()
    print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   MAIN MENU   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
    print()
    typingPrint("   Please select one of the following options:\n")
    print()
    print("     1. Calorie Tracker")
    print("     2. Weight Tracker")
    print("     3. Food Library")
    print()
    
    # Loop repeats until valid input is received
    while True:
        user_input = input("    > ")

        # Calorie Tracker Menu
        if user_input == "1":
            print()
            loadingMenu("           LOADING CALORIE TRACKER, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            calorie_tracker_menu()
            break

        # Weight Tracker Menu
        elif user_input == "2":
            print()
            loadingMenu("           LOADING WEIGHT TRACKER, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            weight_tracker_menu()
            break

        # Food Library Menu
        elif user_input == "3":
            print()
            loadingMenu("           LOADING FOOD LIBRARY, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            food_items_menu()
            break

            # Invalid input raises error
        else:
            validate_data("three_menu_items", user_input)

    return user_input   

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
    print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   CALORIE TRACKER MENU   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
    print()
    print(Fore.GREEN + f"   CURRENT CALORIE GOAL: {round(view_calorie_goal, 2)}")
    print(Fore.YELLOW + f"   REMAINING CALORIES: {round(remaining_calories, 2)}")
    print()
    print(Fore.BLUE + "   CURRENTLY TRACKED ITEMS:")
    print(tabulate(view_calorie_tracker, tablefmt="github"))

    print()
    typingPrint("   Please select one of the following options:\n")
    print()
    print("     1. Update Calorie Goal")
    print("     2. Manually Add Food Item")
    print("     3. Search & Add From Library")
    print("     4. Remove Item From Tracker")
    print("     5. Back to Main Menu")        
    print()
    
    # Loop repeats until valid input is received
    while True:

        user_input = input("    > ")

        # Update Calorie Goal
        if user_input == "1":
            print()
            loadingMenu("           PREPARING TO UPDATE, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            update_calorie_goal()
            break

        # Manually Add Entry, by completing entry steps
        elif user_input == "2":
            print()
            loadingMenu("           PREPARING NEW ITEM, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            add_food_item()
            break

        # Search Food Library and add entry
        elif user_input == "3":
            print()
            loadingMenu("           LOADING FOOD LIBRARY, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            search_food_library()
            break

        # Remove Tracked entries
        elif user_input == "4":
            print()
            loadingMenu("           ACCESSING CALORIE TRACKER, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            remove_tracked_item()
            break

        # Back to Main Menu
        elif user_input == "5":
            print()
            loadingMenu("           LOADING MAIN MENU, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            main_menu()
            break

        # Runs validation with users input
        else:
            validate_data("four_menu_items", user_input)
    
    return user_input   

# Manually add Food Items / Calorie Tracker Menu
def add_food_item():
    """
    Manually adds food item by creating an list entry from each function using user input.
    The final list item is confirmed, the user is able to add list item to tracker and to library.
    """
    new_entry = []

    date = datetime.now()
    date_entry = date.strftime("%d-%m-%Y")
    new_entry.append(date_entry)
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
        print(Fore.BLUE + "   ENTRY PREVIEW")
        print(tabulate(item_table, headers, tablefmt="github"))
        print()

        # Serving Calories
        item_calories_per_g = float(new_entry[3]) / 100
        item_total_calories = [item_calories_per_g * float(new_entry[4])]

        while True:
            print()
            typingPrint("   Please select one of the following options:\n")
            print()
            print("     1. Add Item to Tracker")
            print("     2. Save Item to library")
            print("     3. Back to Calorie Tracker")    
            print()

            user_input = input("    > ")

            if user_input == "1":
                date_meal_name = slice(0,3)
                serving_size = slice(4,5)
                calorie_tracker.append_row(new_entry[date_meal_name] + new_entry[serving_size]  + item_total_calories)
                print()
                loadingMenu("           ADDING ITEM TO TRACKER, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
                clearScreen()
                calorie_tracker_menu()
                break

            elif user_input == "2":
                food_library.append_row(new_entry[2:4])
                print()
                loadingMenu("           ADDING ITEM TO LIBRARY, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
                print()
                clearScreen()
                item_confirmation()
                break

            elif user_input == "3":
                calorie_tracker_menu()
                break
                
            else:
                validate_data("three_menu_items", user_input)

    # Add Serving Size to list
    def item_serving():
        """
        Validates user input to ensure that only numbers are entered
        If valid the entry is added to new_entry list
        """
        while True:
            print()
            typingPrint("   Enter your serving size in grams:\n")
            print()

            user_input = input("    > ")

            item_serving = user_input

            if validate_data("integer", user_input):
                new_entry.append(item_serving)
                clearScreen()
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
            typingPrint("   Enter the amount of Calories(kCal) per 100g\n")
            print("   **NOTE You can get this information from the nutritional label at the back of the product\n")
            print()

            user_input = input("    > ")

            new_calorie = user_input

            if validate_data("integer", user_input):
                new_entry.append(new_calorie)
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
            typingPrint("   Please provide a Name for your food item\n")
            print("   eg Crumb Chicken 'BRAND NAME'\n")
            print()

            user_input = input("    > ")

            new_name = user_input.capitalize()

            if validate_data("item_name", user_input):
                new_entry.append(new_name)
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
            typingPrint("   Please select one of the following options:\n")
            print()
            print("     1. Breakfast")
            print("     2. Lunch")
            print("     3. Dinner")
            print("     4. Snack")        
            print()

            user_input = input("    > ")

            if user_input == "1":
                new_entry.append("Breakfast")
                item_name()
                clearScreen()
                break

            elif user_input == "2":
                new_entry.append("Lunch")
                item_name()
                break

            elif user_input == "3":
                new_entry.append("Dinner")
                item_name()
                break

            elif user_input == "4":
                new_entry.append("Snack")
                item_name()
                break    

            else:
                validate_data("four_menu_items", user_input)

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
        calories_per_g =float(selected_flat_list[3]) / 100
        total_item_calories = calories_per_g * float(selected_flat_list[4])
        selected_flat_list.append(total_item_calories)
        del selected_flat_list[3]

        # Item added to calorie tracker sheet
        calorie_tracker.append_row(selected_flat_list)
        clearScreen()
        search_food_library()

    # Serving size for item
    def search_serving():
        """
        Validates user input to ensure input is a number
        Adds the serving size to the list
        """
        while True:
            print()
            typingPrint("   Enter your serving size in grams:\n")
            print()

            user_input = input("    > ")

            item_serving = user_input

            if validate_data("integer", user_input):
                selected_flat_list.append(item_serving)
                add_search_item()
                print()
                loadingMenu("           ADDING ITEM TO TRACKER, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
                time.sleep(0.5)
                print()
                clearScreen()
                calorie_tracker_menu()

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
            print("     1. Breakfast")
            print("     2. Lunch")
            print("     3. Dinner")
            print("     4. Snack")        
            print()

            user_input = input("    > ")

            if user_input == "1":
                selected_flat_list.insert(0, "Breakfast")
                search_serving()
                clearScreen()
                break

            elif user_input == "2":
                selected_flat_list.insert(0, "Lunch")
                search_serving()
                break

            elif user_input == "3":
                selected_flat_list.insert(0, "Dinner")
                search_serving()
                break

            elif user_input == "4":
                selected_flat_list.insert(0, "Snack")
                search_serving()
                break    

            else:
                validate_data("four_menu_items", user_input)

    # Confirmation of selected item
    def confirm_selected_item():
        """
        Displays the selected item for confirmation
        Provides options to add item, proceeding to next step or return to search
        """
        print()
        print(Fore.BLUE + "   YOUR SELECTION:")
        headers = ["Food Item", "kCal per 100g"]
        print(tabulate(selected_item, headers, tablefmt="github"))

        while True:
            print()
            typingPrint("   Please confirm your selection:\n")
            print()
            print("     1. Add Item to Tracker")
            print("     2. Back to Search")   
            print()

            # flat list is created for next steps so items can be added and list can be tabulated correctly
            global selected_flat_list
            selected_flat_list = [element for innerList in selected_item for element in innerList]

            user_input = input("    > ")

            if user_input == "1":
                clearScreen()
                search_meal()
                break

            elif user_input == "2":
                clearScreen()
                search_food_library()
                break
                
            else:
                validate_data("two_menu_items", user_input)

    # Select Food Item from search_item_list
    def select_food_item():
        """
        Validates user input to ensure that it is a number
        Fetches the item from corresponding index and input
        If there is no item in the index position an error message is displayed
        """
        print()
        typingPrint("   Select a number from the first colum to add food item:\n")
        print()

        global selected_item
        selected_item = []

        while True:

            user_input = int(input("    > "))

            try:
                for i in search_item_list:
                    if user_input == search_item_list.index(i):
                        selected_item.append(search_item_list[user_input])
                        clearScreen()
                        confirm_selected_item()

                for i in search_item_list:
                    if user_input != search_item_list.index(i):
                        raise ValueError("Select a number from the first colum\n")
                    

            except ValueError as e:
                print()
                print(Fore.RED + f"   Invalid data: {e}\n")

    # Main Search Function searches food item sheet for user input
    def search_main():
        """
        Takes user input, validates input to a minimum of 3 characters
        Searches food library sheet for matching items
        If an item is not found an error is displayed and search repeats.
        If item is found the item row is added to a list
        Results are tabulated and displayed
        """
        print()
        # Heading styles from https://textkool.com
        print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   SEARCH FOOD LIBRARY   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
        print()

        while True:
            typingPrint("   Please type the food item you are looking for:\n")
            print()
            print("   Type 'exit' to return to the Calorie Tracker menu")
            print()

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
                    clearScreen()
                    calorie_tracker_menu()

            # Validates search_items, if item could not be found error message is displayed
            def validate_food_search():
                if len(search_items) == 0:
                    print()
                    print(Fore.RED + "   There are no items matching your search criteria")
                    print()
                    search_main()
                
                # If items are found remove possible duplicates and add to search_items_list for tabulate
                else:
                    global search_item_list
                    search_item_list = []

                    # Removes duplicates from list
                    [search_item_list.append(x) for x in search_items if x not in search_item_list]  

                    search_headers = ["Food Item", "kCal per 100g"]
                    search_table = tabulate(search_item_list, search_headers, tablefmt="github", showindex="always")
                    clearScreen()
                    print(Fore.BLUE + "   AVAILABLE OPTIONS:")
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

    print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   REMOVE ITEMS FROM TRACKER   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
    print()
    print(Fore.BLUE + "   CURRENTLY TRACKED ITEMS:")
    print(tabulate(view_calorie_tracker, tablefmt="grid", showindex="always"))
    print()
    typingPrint("   Select a number from the first colum to remove food item:\n")
    print()
    print(Fore.LIGHTWHITE_EX + "   Type 'exit to return to Calorie Tracker'\n")
    print()

    while True:
        
        user_input = input("    > ")

        if user_input == "exit":
            clearScreen()
            calorie_tracker_menu()
            break
        
        try:
            if user_input == "0":
                raise ValueError("Headings can not be removed\n")

            for i in view_calorie_tracker:
                if int(user_input) == view_calorie_tracker.index(i):
                    calorie_tracker.delete_rows(int(user_input)+1)
                    print()
                    loadingMenu("           REMOVING ITEM, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
                    print()
                    clearScreen()
                    remove_tracked_item()

            for i in view_calorie_tracker:
                if int(user_input) != view_calorie_tracker.index(i):
                    raise ValueError("Select a number from the first colum\n")
                
        except ValueError as e:
            print()
            print(Fore.RED + f"   Invalid data: {e}\n")
            
# Input Validation
def validate_data(data, value):
    """
    Validates user input throughout program
    """
    try:       
        # Validates input for two menu items
        if data == "two_menu_items":
            if value != "1" or "2":
                raise ValueError("Select option 1 to 2")

        # Validates input for three menu
        if data == "three_menu_items":
            if value != "1" or "2" or "3":
                raise ValueError("Select option 1 to 3")
            
        # Validates input for four menu    
        elif data == "four_menu_items":
            if value != "1" or "2" or "3" or "4":
                raise ValueError("Select option 1 to 4")
            
        # Validates input for five menu    
        elif data == "four_menu_items":
            if value != "1" or "2" or "3" or "4" or "5":
                raise ValueError("Select option 1 to 5")
        
        # Update Calorie Data Validation 
        elif data == "calorie_data":    
            if not 1500 <= int(value) <= 3500:
                raise ValueError("Select a goal between 1500 and 3500")
        
        elif data == "integer":
            if not int(value):
                raise ValueError("You can only enter numbers")
               
        # Validates string length for item added to tracker and library    
        elif data == "item_name":
            if not value != "" or len(value) > 50 :
                raise ValueError("Category must be between 0 and 50 characters") 

        # Search criteria must be 3 characters or more
        elif data == "search_food_library":
            if len(value) < 3:
                raise ValueError("A minimum of 3 characters required")
            
    except ValueError as e:
            print()
            print(Fore.RED + f"   Invalid data: {e}, please try again.\n")
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
        typingPrint("   Please enter your new calorie goal:\n")
        print()

        user_input = input("    > ")

        if validate_data("calorie_data", user_input):
            print()
            loadingMenu("               UPDATING CALORIE GOAL, PLEASE WAIT...                ".center(110), Fore.BLACK, Back.WHITE)
            print()
            calorie_goal.update_cell(2,2, user_input)
            clearScreen()
            calorie_tracker_menu()
            

            if validate_data("integer", user_input):
                update_calorie_goal()

       
def food_items_menu():
   print("Food Items")

def weight_tracker_menu():
   print("Weight Tracker")


welcome_screen()