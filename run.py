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
food_items = SHEET.worksheet("food_items")



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
    # Loop repeats until valid input is received
    while True:
        print()
        print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   MAIN MENU   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
        print()
        typingPrint("   Please select one of the following options:\n")
        print()
        print("     1. Calorie Goal")
        print("     2. Calorie Tracker")
        print("     3. Weight Tracker")
        print("     4. Food Library")
        print()

        user_input = input("    > ")
         
        # Calorie Goal Menu
        if user_input == "1":
            print()
            loadingMenu("           LOADING CALORIE GOAL, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            calorie_goal_menu()
            break

        # Calorie Tracker Menu
        elif user_input == "2":
            print()
            loadingMenu("           LOADING CALORIE TRACKER, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            calorie_tracker_menu()
            break

        # Weight Tracker Menu
        elif user_input == "3":
            print()
            loadingMenu("           LOADING WEIGHT TRACKER, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            weight_tracker_menu()
            break

        # Food Library Menu
        elif user_input == "4":
            print()
            loadingMenu("           LOADING FOOD LIBRARY, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            food_items_menu()
            break

            # Invalid input raises error
        else:
            validate_data("main_menu", user_input)

    return user_input 
    
def calorie_goal_menu():
    """
    Displays current calorie goal retrieved from sheet.
    Menu items allow users to set a new daily calorie goal and navigate back to main menu
    Validates user input and provides feedback if input is invalid
    """
    # Gets the current calorie goal from worksheet to be displayed
    view_calorie_goal = calorie_goal.cell(2,2, value_render_option='FORMULA').value
    
    # Loop repeats until valid input is received
    while True:
        print()
        # Heading styles from https://textkool.com
        print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   CALORIE GOAL MENU   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
        print()
        print(Fore.GREEN + f"   CURRENT CALORIE GOAL: {view_calorie_goal}")
        print()
        typingPrint("   Please select one of the following options:\n")
        print()
        print("     1. Update Calorie Goal")
        print("     2. Back to Main Menu")
        print()

        user_input = input("    > ")

        # Update Calorie Goal
        if user_input == "1":
            print()
            loadingMenu("           PREPARING TO UPDATE, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            update_calorie_goal()
            break

        # Back to Main Menu
        elif user_input == "2":
            print()
            loadingMenu("           LOADING MAIN MENU, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            main_menu()
            break

        # Runs validation with users input
        else:
            validate_data("calorie_goal_menu", user_input)
    
    return user_input

def calorie_tracker_menu():
    """
    Users ar able to manually enter new item.
    Search and add items from food library.
    View the calorie tracker log or return to the main menu.
    Validates user input and provides feedback if input is invalid
    """
    
    # Loop repeats until valid input is received
    while True:
        print()
        # Heading styles from https://textkool.com
        print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   CALORIE TRACKER MENU   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
        print()
        typingPrint("   Please select one of the following options:\n")
        print()
        print("     1. Manually Add New Item")
        print("     2. Search Food Library")
        print("     3. View Calorie Tracker Log")
        print("     4. Back to Main Menu")
        print()

        user_input = input("    > ")

        # Add New Item to Tracker
        if user_input == "1":
            print()
            loadingMenu("           PREPARING NEW ITEM, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            add_food_item()
            break

        # Search Food Log
        elif user_input == "2":
            print()
            loadingMenu("           LOADING FOOD LIBRARY, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            search_food_library()
            break

        # Back to Main Menu
        elif user_input == "3":
            print()
            loadingMenu("           LOADING CALORIE TRACKER LOG, PLEASE WAIT...           ".center(110), Fore.BLACK, Back.WHITE)
            clearScreen()
            main_menu()
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

    def add_category():
        # Loop repeats until valid input is received
        # Add new date item to new entry
        while True:
            print()
            # Heading styles from https://textkool.com
            print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   ADD CATEGORY   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
            print()
            typingPrint("   Please Enter a Category for your Food Item:\n")
            print("   eg.. Vegetable, Treat, Meat or give it a custom name so that it is easier to find when searching library\n")
            print()

            user_input = input("    > ")

            new_category = user_input

            if validate_data("add_category", user_input):
                new_entry.append(new_category)
                clearScreen()
                print_new_entry()
                return new_category
    
    
    def print_new_entry():
        print(new_entry)


    def item_date():
    # Loop repeats until valid input is received
    # Add new category to new entry
        while True:
            print()
            # Heading styles from https://textkool.com
            print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   ADD ITEM   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
            print()
            typingPrint("   Please Enter Date for log entry:\n")
            typingPrint("   Date format must be DD-MM-YYYY\n")
            print()

            user_input = input("    > ")

            new_date = user_input

            if validate_data("item_date", user_input):
                clearScreen()
                new_entry.append(new_date)
                add_category()
                return new_date
            break

    item_date()

def search_food_library():
    """
    """
    print()
    # Heading styles from https://textkool.com
    print(Fore.WHITE + "   ▌│█║▌║▌║▌│█║▌║▌║" + Fore.BLUE + "   SEARCH FOOD LIBRARY   " + Fore.WHITE + "║▌║▌║█│▌▌│█║▌║▌║")
    print()

    def select_food_item():
        print()
        typingPrint("   Select a number from the first colum to add food item:\n")
        print()

        user_input = int(input("    > "))

        selected_item = []
        
        for i in search_item_list:
            if user_input == search_item_list.index(i):
                selected_item.append(search_item_list[user_input])
                if user_input != search_item_list.index(i):
                    print("   Select a number from the first colum:\n")
        
        clearScreen()
        print()
        print("   You have selected the following item:")
        print()
        headers = ["Category", "Food Item", "Total kCal"]
        print(tabulate(selected_item, headers, tablefmt="grid"))
        print()


    # Loop repeats until valid input is received
    while True:
        typingPrint("   Please type the food item you are looking for:\n")

        print()

        user_input = input("    > ")

        if validate_data("search_food_library", user_input): 
            search_items = re.compile(user_input.capitalize())
            get_food_items = food_items.findall(search_items)
            
            search_items = []
            
            for x in get_food_items:
                item = x._row
                item_row = food_items.row_values(item)
                search_items.append(item_row)

            def validate_food_search():
                if len(search_items) == 0:
                    print()
                    print(Fore.RED + "   There are no items matching your search criteria")
                    print()
            
                else:
                    # Removes duplicates from list    
                    global search_item_list
                    search_item_list = []
                    [search_item_list.append(x) for x in search_items if x not in search_item_list]  

                    search_headers = ["Category", "Food Item", "Total kCal"]
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
            if value != "1" or "2" or "3" or "4":
                raise ValueError("Select option 1 to 4")
        
        # Calorie Goal Menu Validation
        elif data == "calorie_goal_menu":
            if value != "1" or "2":
                raise ValueError("Select option 1 or 2")
        
        # Update Calorie Data Validation    
        elif data == "calorie_data":
            if not (1500 <= value <= 3500):
                raise ValueError("Select a goal between 1500 and 3500")
        
        # Calorie Tracker Menu Validation    
        elif data == "calorie_tracker_menu":
            if value != "1" or "2" or "3" or "4":
                raise ValueError("Select option 1 to 3")

        # Add New Item, Date Format Validation    
        elif data == "item_date":
            format = "%d-%m-%Y"
            if not datetime.strptime(value, format):
                raise ValueError("Please enter date in correct format DD-MM-YYYY")
        
        # Add New Item, Category Format Validation 
        elif data == "add_category":
            if not value != "" and len(value) < 20 :
                raise ValueError("Category must be between 0 and 30 characters")
            
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
            calorie_goal_menu()
            break
    

    
        


def food_items_menu():
   print("Food Items")

def weight_tracker_menu():
   print("Weight Tracker")






main()