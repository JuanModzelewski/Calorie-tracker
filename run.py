# Libraries
import os
import sys
import time

import colorama
import gspread
import re

from collections import defaultdict
from colorama import Back, Fore, Style
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from datetime import datetime

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

    print("Welcome to Calorie Tracker.\n".center(110))
    ##loadingMenu("           LOADING MENU, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
    print()
    time.sleep(0.5)


def main():
    welcome_screen()
    menu_navigation()
    


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


def main_menu():
    """
    Runs the main menu of the program.
    Allows users to navigate through program.
    Validates user input and provides feedback if input is invalid
    """
    print()
    print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   MAIN MENU   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
    
    # Loop repeats until valid input is received
    while True:
        print()
        typingPrint("   Please select one of the following options:\n")
        print()
        print("     1. Calorie Tracker")
        print("     2. Weight Tracker")
        print("     3. Food Library")
        print()

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
            validate_data("main_menu", user_input)

    return user_input   

def calorie_tracker_menu():
    """
    Users ar able to manually enter new item.
    Search and add items from food library.
    View the calorie tracker log or return to the main menu.
    Validates user input and provides feedback if input is invalid
    """
    view_calorie_goal = calorie_goal.cell(2,2, value_render_option='FORMULA').value
    view_calorie_tracker = calorie_tracker.get_all_values()

    print()
    # Heading styles from https://textkool.com
    print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   CALORIE TRACKER MENU   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
    print()
    print(Fore.GREEN + f"   CURRENT CALORIE GOAL: {view_calorie_goal}")
    print()
    print(Fore.GREEN + f"   CURRENT CALORIE GOAL: {view_calorie_goal}")
    print()
    print(Fore.BLUE + "   CURRENTLY TRACKED ITEMS")
    print(tabulate(view_calorie_tracker, tablefmt="grid"))
    
    # Loop repeats until valid input is received
    while True:
        print()
        typingPrint("   Please select one of the following options:\n")
        print()
        print("     1. Update Calorie Goal")
        print("     2. Manually Add Food Item")
        print("     3. Search & Add From Library")
        print("     4. Back to Main Menu")        
        print()
        user_input = input("    > ")


        # Add New Item to Tracker
        if user_input == "1":
            print()
            loadingMenu("           PREPARING TO UPDATE, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            update_calorie_goal()
            break

        # Search Food Log
        elif user_input == "2":
            print()
            loadingMenu("           PREPARING NEW ITEM, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            add_food_item()
            break

        # Back to Main Menu
        elif user_input == "3":
            print()
            loadingMenu("           LOADING FOOD LIBRARY, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            search_food_library()
            break

    # Back to Main Menu
        elif user_input == "4":
            print()
            loadingMenu("           LOADING MAIN MENU, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            main_menu()
            break

        # Runs validation with users input
        else:
            validate_data("calorie_tracker_menu", user_input)
    
    return user_input   

def add_food_item():
    """
    Manually adds food item by creating an entry from each function using user input.
    Each function requires a different method of validation
    """
    new_entry = []

    date = datetime.now()
    date_entry = date.strftime("%d-%m-%Y")
    new_entry.append(date_entry)
    item_table = []
    item_table.append(new_entry)
    headers = ["Date", "Meal", "Category", "Name", "kCal per 100g", "Serving Size (g)"]

    def item_confirmation():
        """
        """
        print()
        print(Fore.BLUE + "   ENTRY PREVIEW")
        print(tabulate(item_table, headers, tablefmt="grid"))
        print()

        item_calories_per_g = int(new_entry[4]) / 100
        item_total_calories = [item_calories_per_g * int(new_entry[5])]

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
                date = slice(0,2)
                meal_name = slice(3,4)
                serving_size = slice(5,6)
                calorie_tracker.append_row(new_entry[date] + new_entry[meal_name] + new_entry[serving_size] + item_total_calories)
                loadingMenu("           ADDING ITEM TO TRACKER, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
                clearScreen()
                calorie_tracker_menu()
                break

            elif user_input == "2":
                food_library.append_row(new_entry[2:5])
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
                validate_data("item_confirmation", user_input)

    def item_serving():
        """
        """
        while True:
            print()
            typingPrint("   Enter your serving size in grams:\n")
            print()

            user_input = input("    > ")

            item_serving = user_input

            if validate_data("item_serving", user_input):
                new_entry.append(item_serving)
                clearScreen()
                item_confirmation()
                break
                
    def item_calories():
        """
        """
        while True:
            print()
            typingPrint("   Enter the amount of Calories(kCal) per 100g\n")
            print("   **NOTE You can get this information from the nutritional label at the back of the product\n")
            print()

            user_input = input("    > ")

            new_calorie = user_input

            if validate_data("item_calories", user_input):
                new_entry.append(new_calorie)
                item_serving()
                break

    def item_name():
        """
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

    def item_category():
        """
        """
        while True:
            print()
            typingPrint("   Please Enter a Category for your Food Item:\n")
            print("   eg Fruit, Vegetable, Grains, Meat, \n")
            print()

            user_input = input("    > ")

            new_category = user_input.capitalize()

            if validate_data("item_category", user_input):
                new_entry.append(new_category)
                item_name()
                break

    def item_meal():
        """
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
                item_category()
                clearScreen()
                break

            elif user_input == "2":
                new_entry.append("Lunch")
                item_category()
                break

            elif user_input == "3":
                new_entry.append("Dinner")
                item_category()
                break

            elif user_input == "4":
                new_entry.append("Snack")
                item_category()
                break    

            else:
                validate_data("item_meal", user_input)

    item_meal()   

def search_food_library():
    """
    """
    def add_search_item():
        date = datetime.now()
        date_entry = date.strftime("%d-%m-%Y")
        selected_flat_list.insert(0, date_entry)
        del selected_flat_list[2]
        calories_per_g =float(selected_flat_list[3]) / 100
        total_item_calories = calories_per_g * float(selected_flat_list[4])
        selected_flat_list.append(total_item_calories)
        del selected_flat_list[3]
        calorie_tracker.append_row(selected_flat_list)

    def search_serving():
        """
        """
        while True:
            print()
            typingPrint("   Enter your serving size in grams:\n")
            print()

            user_input = input("    > ")

            item_serving = user_input

            if validate_data("item_serving", user_input):
                selected_flat_list.append(item_serving)
                add_search_item()
                print()
                loadingMenu("           ADDING ITEM TO TRACKER, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
                time.sleep(0.5)
                print()
                clearScreen()
                calorie_tracker_menu()
                

    def search_meal():
        """
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
                validate_data("item_meal", user_input)

    def add_selected_item():
        print()
        print(Fore.BLUE + "   YOUR SELECTION:")
        headers = ["Category", "Food Item", "kCal per 100g"]
        print(tabulate(selected_item, headers, tablefmt="grid"))
        print()

        while True:
            print()
            typingPrint("   Please select one of the following options:\n")
            print()
            print("     1. Add Item to Tracker")
            print("     2. Back to Search")   
            print()

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
                validate_data("item_confirmation", user_input)

    def select_food_item():
        print()
        typingPrint("   Select a number from the first colum to add food item:\n")
        print()

        global selected_item
        selected_item = []

        user_input = int(input("    > "))
        
        for i in search_item_list:
            if user_input == search_item_list.index(i):
                selected_item.append(search_item_list[user_input])
                if user_input != search_item_list.index(i):
                    print("   Select a number from the first colum:\n")
        
        clearScreen()
        add_selected_item()

    # Loop repeats until valid input is received
    print()
    # Heading styles from https://textkool.com
    print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   SEARCH FOOD LIBRARY   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
    print()

    while True:
        typingPrint("   Please type the food item you are looking for:\n")

        print()

        user_input = input("    > ")

        if validate_data("search_food_library", user_input): 
            search_items = re.compile(user_input.capitalize())
            get_food_items = food_library.findall(search_items)
            
            search_items = []
            
            for x in get_food_items:
                item = x._row
                item_row = food_library.row_values(item)
                search_items.append(item_row)

            def validate_food_search():
                if len(search_items) == 0:
                    print()
                    print(Fore.RED + "   There are no items matching your search criteria")
                    print()
                    search_food_library()

                else:
                    # Removes duplicates from list    
                    global search_item_list
                    search_item_list = []
                    [search_item_list.append(x) for x in search_items if x not in search_item_list]  

                    search_headers = ["Category", "Food Item", "kCal per 100g"]
                    search_table = tabulate(search_item_list, search_headers, tablefmt="grid", showindex="always")
                    print(search_table)
                    select_food_item()
            
            validate_food_search()

        return False

def validate_data(data, value):
    """
    Validates user input
    """
    try:
        # Main Menu Validation  
        if data == "main_menu":
            if value != "1" or "2" or "3":
                raise ValueError("Select option 1 to 3")
        
        # Update Calorie Data Validation    
        elif data == "calorie_data":
            if not (1500 <= value <= 3500):
                raise ValueError("Select a goal between 1500 and 3500")
        
        # Calorie Tracker Menu Validation    
        elif data == "calorie_tracker_menu":
            if value != "1" or "2" or "3" or "4":
                raise ValueError("Select option 1 to 4")
            
        # Item Meal selection Validation    
        elif data == "item_meal":
            if value != "1" or "2" or "3" or "4":
                raise ValueError("Select option 1 to 4")
 
        # Add New Item, Category Format Validation 
        elif data == "item_category":
            if not value != "" or len(value) > 20 :
                raise ValueError("Category must be between 0 and 20 characters")
            
        elif data == "item_name":
            if not value != "" or len(value) > 30 :
                raise ValueError("Category must be between 0 and 30 characters")
            
        elif data == "item_calories":
            if not int(value):
                raise ValueError("You can only enter numbers")
            
        elif data == "item_serving":
            if not int(value):
                raise ValueError("You can only enter numbers")

        elif data == "item_confirmation":
            if value != "1" or "2" or "3":
                raise ValueError("Select option 1 to 3")          


        # 
        elif data == "search_food_library":
            if len(value) < 3 :
                raise ValueError("Search must be greater than 3 characters")
            
    except ValueError as e:
            print()
            print(Fore.RED + f"   Invalid data: {e}, please try again.\n")
            return False
         
    return True
    
def update_calorie_goal():
    while True:
        print()
        typingPrint("   Please enter your new calorie goal:\n")
        print()
        user_input = int(input("    > "))

        if validate_data("calorie_data", user_input):
            print()
            loadingMenu("               UPDATING CALORIE GOAL, PLEASE WAIT...                ".center(110), Fore.BLACK, Back.WHITE)
            print()
            calorie_goal.update_cell(2,2, user_input)
            clearScreen()
            calorie_tracker_menu()
    

    
        


def food_items_menu():
   print("Food Items")

def weight_tracker_menu():
   print("Weight Tracker")






main()