# Libraries
import colorama
import gspread
import re
from datetime import datetime
from colorama import Fore
from google.oauth2.service_account import Credentials
from tabulate import tabulate


from utilities import (loading_menu, validate_data, request,
                       menu_headings, clear_screen, information, example)


from constants import (DATA_TYPE, HEADERS, SPACING, MENU_ITEMS,
                       CALORIE_TRACKER_LOGO)

# Initialize colorama for text formatting
# https://linuxhint.com/colorama-python/
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

# GSPREAD SHEETS
calorie_tracker = SHEET.worksheet("calorie_tracker")
calorie_goal = SHEET.worksheet("calorie_goal")
weight_tracker = SHEET.worksheet("weight_tracker")
food_library = SHEET.worksheet("food_items")


def welcome_screen():
    """
    Displays Banner and welcome message
    """
    # ASCII art generator: https://manytools.org/hacker-tools/ascii-banner/
    CALORIE_TRACKER_LOGO

    print(Fore.BLUE + "WELCOME TO CALORIE TRACKER".center(70))
    print("Your daily calorie tracking tool to ensure you meet your"
          .center(70))
    print("calorie requirements and achieve you goals.\n".center(70))
    print(Fore.BLUE + "GETTING STARTED".center(70))
    print("Set your calorie goal in the calorie tracker menu.".center(70))
    print("Manually add an entry or search and add from the Food Library."
          .center(70))
    print("Items can be added to Food Library by Manually adding".center(70))
    print("an item and choosing to save the item to the library.".center(70))
    print()
    input(Fore.GREEN + "PRESS ENTER TO CONTINUE".center(70))

    loading_menu("LOADING CALORIE TRACKER")
    calorie_tracker_menu()


# Searches google sheets for values in date criteria and
# builds a list from entries
def retrieve_values():
    """
    Uses the current date to find values in google sheets
    Compiles a list from found items
    List are used to tabulate the main Calorie tracker,
    Remove items table
    """
    date = datetime.now()
    global current_date
    current_date = date.strftime("%d-%m-%Y")

    global tracker_date
    tracker_date = calorie_tracker.findall(current_date)

    global tracker_entries
    tracker_entries = []

    global row_id
    row_id = []

    # Loops through the calorie_tracker sheet and gets row values
    for x in tracker_date:
        item = x._row
        item_row = calorie_tracker.row_values(item)
        tracker_entries.append(item_row)

    # Removes the date of from each entry // saving space on terminal
    for x in tracker_entries:
        del x[0]

    # Creates the index list to add to tabulate with index staring at 1
    for i in tracker_date:
        row_id.append(tracker_date.index(i) + 1)


# Creates tables for Calorie Tracker and Remove items selection
def tracker_table(menu):
    """
    Creates the Main tables for Calorie Tracker and Remove Items Menus
    Entries are taken from the calorie_tacker sheet using findall,
    with date as search criteria
    Entries are modified and displayed
    """
    retrieve_values()

    # If there are no entries prints feedback
    if tracker_entries == []:
        print("*****  NO ENTRIES FOR TODAY  *****".center(60))

    # Main table fro Calorie Tracker
    elif menu == "tracker_menu":
        print(tabulate(tracker_entries,
                       HEADERS.TRACKER_HEADERS,
                       tablefmt="rst",
                       maxcolwidths=[10, 40, 7, 7],
                       colalign=("left", "left", "center", "center")))

    # Table for Remove Items displayed with indexes
    elif menu == "remove_items_menu":
        print(tabulate(tracker_entries,
                       HEADERS.REMOVE_ITEMS_HEADER,
                       tablefmt="rst",
                       maxcolwidths=[5, 10, 35, 7, 7],
                       colalign=("center", "left", "left", "center", "center"),
                       showindex=row_id))


# Calorie Tracker Menu
def calorie_tracker_menu():
    """
    Users are given options to:
    Change the calorie goal
    Manually add a new item by following steps to create a new entry
    Search and add items from food library
    Remove Tracked items
    User input is validated, function taken from utilities.py
    """
    retrieve_values()

    calorie_values = []

    # Gets the Calorie Goal value from the calorie_goal sheet
    view_calorie_goal = calorie_goal.cell(
        2, 2, value_render_option='FORMULA').value

    # Loops through lis and gets all calorie indexes
    for i in tracker_entries:
        calorie_values.append(i[3])

    # Converts the list strings into float numbers
    calories_list = [float(i) for i in calorie_values]
    # Sum of calorie list
    total_calories = sum(calories_list)

    # Calculation for remaining Calories
    remaining_calories = view_calorie_goal - total_calories

    print()
    menu_headings("CALORIE TRACKER MENU")
    print(Fore.BLUE + f"CURRENTLY TRACKED ITEMS: {current_date}\n")
    tracker_table("tracker_menu")
    print()
    print(Fore.GREEN + f"CURRENT CALORIE GOAL: {round(view_calorie_goal, 2)}" +
          SPACING.EIGHT_SPACE + Fore.YELLOW +
          f"REMAINING CALORIES: {round(remaining_calories, 2)}\n")

    request("Select one of following options:\n")

    # Generates a list of options using the selected menu items
    for idx, menu_item in enumerate(MENU_ITEMS.CALORIE_TRACKER_MENU):
        print(SPACING.FIVE_SPACE + str(idx + 1) + ". " + menu_item)
    print()

    # Loop repeats until valid input is received
    while True:

        user_input = input("    > ")

        if user_input == "1":
            loading_menu("LOADING CALORIE GOAL")
            update_calorie_goal()
            break

        elif user_input == "2":
            loading_menu("PREPARING NEW ITEM")
            entry_meal("manual_entry")
            break

        elif user_input == "3":
            loading_menu("PREPARING TO SEARCH")
            search_main()
            break

        elif user_input == "4":
            loading_menu("LOADING ITEMS")
            remove_tracked_item()
            break

        else:
            validate_data(DATA_TYPE.FOUR_MENU_ITEMS, user_input)


# Adds a meal timing to list entry based method used
def entry_meal(method):
    """
    Validates user input to ensure only available options are entered
    Add the selected a list, the list chosen list is decided by the method
    """
    global new_entry
    new_entry = []

    print()
    request("Please select one of the following options:\n")
    information("Type 'exit' to return to Calorie Tracker Menu\n")

    # Generates a list of options using the selected menu items
    # ["Breakfast", "Lunch", "Dinner", "Snack"]
    for idx, meal in enumerate(MENU_ITEMS.MEAL_TYPES):
        print(SPACING.FIVE_SPACE + str(idx + 1) + ". " + meal)
    print()

    while True:

        user_input = input("    > ")

        if user_input.lower() == "exit":
            loading_menu("LOADING CALORIE TRACKER")
            calorie_tracker_menu()
            break

        elif user_input in ["1", "2", "3", "4"]:
            if method == "search_entry":
                selected_flat_list.insert(
                    0, MENU_ITEMS.MEAL_TYPES[int(user_input) - 1])
                clear_screen()
                entry_serving("search_entry")
                break

            elif method == "manual_entry":
                new_entry.insert(
                    1, MENU_ITEMS.MEAL_TYPES[int(user_input) - 1])
                clear_screen()
                name_manual_item()
                break

        else:
            validate_data(DATA_TYPE.FOUR_MENU_ITEMS, user_input)


# Pushes final entry to google sheets based on method used
def add_item(method):
    """
    Compile and append entry to google sheet based on the entry method
    """
    date = datetime.now()
    date_entry = date.strftime("%d-%m-%Y")

    if method == "manual_entry":
        item_total_calories = [(float(new_entry[2]) / 100) *
                               float(new_entry[3])]
        new_entry.insert(0, date_entry)
        date_meal_name = slice(0, 3)
        serving_size = slice(4, 5)
        calorie_tracker.append_row(new_entry[date_meal_name] +
                                   new_entry[serving_size] +
                                   item_total_calories)

    elif method == "search_entry":
        date = datetime.now()
        date_entry = date.strftime("%d-%m-%Y")
        selected_flat_list.insert(0, date_entry)

        # Calculation for total calories for search entry method
        total_item_calories = (
            float(selected_flat_list[3]) / 100) * float(selected_flat_list[4])
        selected_flat_list.append(total_item_calories)
        # Removes the calories per 100g entry
        del selected_flat_list[3]

        # Item added to calorie tracker sheet
        calorie_tracker.append_row(selected_flat_list)
        print()
        loading_menu("ADDING ITEM TO TRACKER")
        calorie_tracker_menu()


# Add serving size to list based on method used
def entry_serving(method):
    """
    Validates user input to ensure input is a number
    Adds the serving size to a list based on method
    """
    print()
    request("Enter your serving size in grams:\n")
    information("Type 'exit' to return to Calorie Tracker Menu\n")

    while True:

        user_input = input(f"{SPACING.THREE_SPACE} Serving Size: ")

        if user_input.lower() == "exit":
            loading_menu("LOADING CALORIE TRACKER")
            calorie_tracker_menu()
            break

        elif validate_data(DATA_TYPE.INTEGER, user_input):
            if method == "search_entry":
                selected_flat_list.append(int(user_input))
                add_item("search_entry")
                loading_menu("ADDING ITEM TO TRACKER")
                calorie_tracker_menu()
                break

            elif method == "manual_entry":
                new_entry.append(int(user_input))
                clear_screen()
                confirm_manual_item()
                break


# Confirm Item Information, add to Tracker and Library
def confirm_manual_item():
    """
    new_entry list is tabulated and displayed as a preview.
    Calculation for item calories is done by dividing calories
    per 100g by 100 and multiplying by serving size.
    The user is given options to add item to tracker or add item to library.
    If Add item to Tracker is selected the required indexes are taken from
    new_entry list and added to calorie_tracker sheet.
    If Save Item to library is selected the required indexes are taken from
    new_entry list and added to food_library sheet.

    """
    # Table displaying item to be added
    item_table = []
    item_table.append(new_entry)

    print()
    print(Fore.BLUE + "ENTRY PREVIEW: ")
    print(tabulate(item_table, HEADERS.CONFIRM_MANUAL_ITEM_HEADER,
                   tablefmt="rst",
                   maxcolwidths=[10, 40, 7, 7],
                   colalign=("left", "left", "center", "center")))
    print()

    # Serving Calories
    request("Please select one of the following options:\n")

    # Generates a list of options using the selected menu items
    # ["Add Item to Tracker",
    # "Save Item to library",
    # "Back to Calorie Tracker"]
    for idx, menu_item in enumerate(MENU_ITEMS.ITEM_CONFIRMATION_SELECTION):
        print(SPACING.FIVE_SPACE + str(idx + 1) + ". " + menu_item)
    print()

    while True:

        user_input = input(f"{SPACING.THREE_SPACE} > ")

        # Add item to Tracker
        if user_input == "1":
            # Calculations are done in the add_item function
            add_item("manual_entry")
            loading_menu("ADDING ITEM TO TRACKER")
            calorie_tracker_menu()
            break

        # Save item to library
        elif user_input == "2":
            food_library.append_row(new_entry[1:3])
            loading_menu("ADDING ITEM TO LIBRARY")
            confirm_manual_item()
            break

        # Back to Calorie Tracker
        elif user_input == "3":
            loading_menu("LOADING CALORIE TRACKER")
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
    print()
    request("Enter the amount of Calories(kCal) per 100g:")
    example("**NOTE You can get this information from the nutritional label")
    example("at the back of the product\n")
    information("Type 'exit' to return to Calorie Tracker Menu\n")

    while True:

        user_input = input(f"{SPACING.THREE_SPACE} Calories: ")

        if user_input.lower() == "exit":
            loading_menu("LOADING CALORIE TRACKER")
            clear_screen()
            calorie_tracker_menu()
            break

        elif validate_data(DATA_TYPE.INTEGER, user_input):
            new_entry.append(int(user_input))
            clear_screen()
            entry_serving("manual_entry")
            break


# Add Item Name to list
def name_manual_item():
    """
    The users input is validated to ensure the entry is not blank,
    and no more than 50 character
    If the entry is valid the entry is added to the new_entry list
    """
    print()
    request("Please provide a Name for your food item")
    example("eg Crumb Chicken 'BRAND NAME' (grams per item)\n")
    information("Type 'exit' to return to Calorie Tracker Menu\n")

    while True:

        user_input = input(f"{SPACING.THREE_SPACE} Item Name: ")

        if user_input.lower() == "exit":
            loading_menu("LOADING CALORIE TRACKER")
            clear_screen()
            calorie_tracker_menu()
            break

        elif validate_data(DATA_TYPE.ENTRY_NAME, user_input):
            new_entry.append(user_input.title())
            clear_screen()
            calories_manual_item()
            break


# Confirm selected item
def confirm_search_item():
    """
    Displays the selected item for confirmation
    Provides options to add item, proceeding to next step or return to search
    """
    print()
    print(Fore.BLUE + "YOUR SELECTION:")
    print(tabulate(selected_item,
                   HEADERS.CONFIRM_SEARCH_ITEM_HEADER,
                   tablefmt="rst",
                   maxcolwidths=[40, 10],
                   colalign=("left", "center")))
    print()
    request("Please confirm your selection\n")
    information("Type 'exit' to return to Calorie Tracker Menu\n")

    while True:

        # Generates a list of options using the selected menu items
        # ["Add Item to Tracker", "Back to Search"]
        for idx, menu_item in enumerate(
                MENU_ITEMS.SEARCH_CONFIRMATION_SELECTION):
            print(SPACING.FIVE_SPACE + str(idx + 1) + ". " + menu_item)
        print()

        # flat list is created for next steps so items can be added
        # And list can be tabulated correctly
        global selected_flat_list
        selected_flat_list = [
            element for innerList in selected_item for element in innerList]

        user_input = input(f"{SPACING.THREE_SPACE} > ")

        # Add Item to Tracker
        if user_input == "1":
            clear_screen()
            entry_meal("search_entry")
            break

        # Back to Search
        elif user_input == "2":
            clear_screen()
            search_main()
            break

        elif user_input.lower() == "exit":
            loading_menu("LOADING CALORIE TRACKER")
            calorie_tracker_menu()
            break

        else:
            validate_data(DATA_TYPE.TWO_MENU_ITEMS, user_input)


# Select an item from the search results
def select_search_item():
    """
    Validates user input to ensure that it is a number
    Fetches the item from corresponding index and input
    If there is no item in the index position an error message is displayed
    """
    print()
    request("Select a number from the Item No. Colum to add food entry:\n")
    information("Type 'exit' to return to Calorie Tracker Menu\n")

    global selected_item
    selected_item = []

    while True:

        user_input = input(f"{SPACING.THREE_SPACE} > ")

        if user_input.lower() == "exit":
            loading_menu("LOADING CALORIE TRACKER")
            calorie_tracker_menu()
            break

        try:
            for i in search_item_list:
                if int(user_input) == search_item_list.index(i) + 1:
                    selected_item.append(search_item_list[int(user_input) - 1])
                    clear_screen()
                    confirm_search_item()
                    break

            for i in search_item_list:
                if int(user_input) != search_item_list.index(i) + 1:
                    raise ValueError(
                        "Select a number from the Item No. colum\n")

        except ValueError as e:
            print()
            print(Fore.RED + SPACING.THREE_SPACE + f"Invalid data: {e}\n")


# Search food_item sheet validate and display results
def search_main():
    """
    Takes user input, validates input to a minimum of 3 characters
    Searches food library sheet for matching items
    If an item is not found an error is displayed and search repeats.
    If item is found the item row is added to a list
    Results are tabulated and displayed
    """
    global search_item_list
    search_item_list = []

    print()
    menu_headings("SEARCH FOOD LIBRARY")
    request("Please type the food item you are looking for:\n")
    information("Type 'exit' to return to Calorie Tracker Menu\n")

    while True:

        user_input = input(f"{SPACING.THREE_SPACE} Search for: ")

        # Allows user to exit search
        if user_input.lower() == "exit":
            loading_menu("LOADING CALORIE TRACKER")
            calorie_tracker_menu()
            break

        # Find all instances of user input in sheet
        elif validate_data(DATA_TYPE.SEARCH_CRITERIA, user_input):
            search_items = re.compile(user_input.title())
            get_food_items = food_library.findall(search_items)

            search_items = []

            # Loop through all instances and add items row to search_items list
            for x in get_food_items:
                item = x._row
                item_row = food_library.row_values(item)
                search_items.append(item_row)

            # Validates search_items, if item could not be found
            # error message is displayed
            if len(search_items) == 0:
                print()
                clear_screen()
                print(SPACING.THREE_SPACE + Fore.RED +
                      "There are no items matching your search criteria")
                print()
                search_main()

            else:
                # Removes duplicates from list
                [search_item_list.append(x)
                 for x in search_items if x not in search_item_list]

                search_row_id = []

                for i in search_item_list:
                    search_row_id.append(search_item_list.index(i)+1)

                loading_menu("SEARCHING LIBRARY")
                print(Fore.BLUE + "AVAILABLE OPTIONS:")
                print(tabulate(search_item_list,
                               HEADERS.SEARCH_HEADERS,
                               tablefmt="rst",
                               maxcolwidths=[5, 40, 10],
                               colalign=("center", "left", "center"),
                               showindex=search_row_id))
                select_search_item()


# Removes items from Tracker
def remove_tracked_item():
    """
    Allows user to remove items from calorie tracker.
    Tabulates tracker and displays item indexes.
    Unavailable Item No. cannot be selected,
    and only numbers can be entered.
    If input is valid items from corresponding row are removed.
    """
    print()
    menu_headings("REMOVE ITEMS MENU")
    print(Fore.BLUE + "CURRENTLY TRACKED ITEMS:")
    print()
    tracker_table("remove_items_menu")
    print()
    request("Select a number from the Item No. Colum to remove")
    request("corresponding Food Entry:\n")
    information("Type 'exit' to return to Calorie Tracker Menu\n")

    while True:

        user_input = input(f"{SPACING.THREE_SPACE} Remove Item No. : ")

        if user_input.lower() == "exit":
            loading_menu("LOADING CALORIE TRACKER")
            calorie_tracker_menu()
            break

        try:
            for i in tracker_date:
                current_entries = (len(calorie_tracker.get_all_values()) -
                                   len(tracker_date))
                remove_row = int(user_input) + int(current_entries)

                if int(user_input) - 1 == tracker_date.index(i):
                    calorie_tracker.delete_rows(remove_row)
                    loading_menu("REMOVING ITEM")
                    remove_tracked_item()
                    break

            for i in tracker_date:
                if int(user_input) != tracker_date.index(i):
                    raise ValueError("Select a number from the Item No. colum")

        except ValueError as e:
            print()
            print(Fore.RED + SPACING.THREE_SPACE + f"Invalid data: {e}\n")


# Update Calorie Goal / Calories Tracker Menu
def update_calorie_goal():
    """
    Allow user to set new calorie goal
    Validates user input to ensure goal is realistic,
    between 1500 and 3500 calories
    Updated cell on Calorie Goal sheet
    """
    print()
    menu_headings("UPDATE CALORIE GOAL")
    request("Please enter your new calorie goal:\n")
    information("Type 'exit' to return to Calorie Tracker\n")

    while True:

        user_input = input("    > ")

        if user_input.lower() == "exit":
            loading_menu("LOADING CALORIE TRACKER")
            calorie_tracker_menu()
            break

        if validate_data(DATA_TYPE.CALORIE_RANGE, user_input):
            calorie_goal.update_cell(2, 2, user_input)
            loading_menu("UPDATING CALORIE GOAL")
            calorie_tracker_menu()

            if validate_data(DATA_TYPE.INTEGER, user_input):
                update_calorie_goal()
            break


def main():
    welcome_screen()


main()
