import os

# https://pypi.org/project/colorama/
from colorama import Back, Fore, Style

import sys
import time
from constants import DATA_TYPE, SPACING, MENU_HEADING_STYLE

# Assistance with setup and formatting from GeeksforGeeks
# https://www.geeksforgeeks.org/fontstyle-module-in-python/
import fontstyle 

# Creates the loading style
def loading_style(text, text_color = Fore.BLACK, background_color = Back.WHITE):
    for character in text:
        sys.stdout.write(text_color + background_color + character)
        sys.stdout.flush()
        time.sleep(0.01)

# Brief pause before clearing screen
def pause_clear():
    """
    Clears screen after a brief pause.
    """
    time.sleep(1.5)
    clear_screen()

# Clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[2J')

# Menu Headings styling
def menu_headings(title):
    print(f"{SPACING.EIGHT_SPACE}{MENU_HEADING_STYLE}  {title}  {MENU_HEADING_STYLE}".center(70))
    print()

# Requesting user input styling
def request(string):
    text = fontstyle.apply(string, "BOLD")
    print(SPACING.THREE_SPACE + text)

# Example for request styling
def example(string):
    text = fontstyle.apply(string, "ITALIC")
    print(SPACING.THREE_SPACE + text)

# Styling for any other information displayed
def information(text):
    print(SPACING.THREE_SPACE + Style.DIM +  text)

# Uses loading style and text string to generate loading animation
def loading_menu(text):
        print()
        loading_style(f"{SPACING.TWELVE_SPACE} {text}, PLEASE WAIT {SPACING.TWELVE_SPACE}".center(70), Fore.GREEN, Back.BLACK)
        pause_clear()

# Menu Input Validation
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
        if data == DATA_TYPE.TWO_MENU_ITEMS:
            menu_input_validation(value, 2)

        # Validates input for three menu
        elif data == DATA_TYPE.THREE_MENU_ITEMS:
            menu_input_validation(value, 3)
            
        # Validates input for four menu    
        elif data == DATA_TYPE.FOUR_MENU_ITEMS:
            menu_input_validation(value, 4)
            
        # Validates input for five menu    
        elif data == DATA_TYPE.FIVE_MENU_ITEMS:
            menu_input_validation(value, 5)
        
        # Update Calorie Data Validation 
        elif data == DATA_TYPE.CALORIE_RANGE:    
            if not DATA_TYPE.MIN_CALORIES <= int(value) <= DATA_TYPE.MAX_CALORIE:
                raise ValueError("Select a goal between 1500 and 3500")
        
        elif data == DATA_TYPE.INTEGER:
            if not int(value):
                raise ValueError("You can only enter numbers")
               
        # Validates string length for item added to tracker and library    
        elif data == DATA_TYPE.ENTRY_NAME:
            if not 5 <= len(value) <= 50 :
                raise ValueError("Item Name must be between 5 and 50 characters") 

        # Search criteria must be 3 characters or more
        elif data == DATA_TYPE.SEARCH_CRITERIA:
            if len(value) < 3:
                raise ValueError("A minimum of 3 characters required")
            
    except ValueError as e:
            print()
            print(Fore.RED + SPACING.THREE_SPACE + f"Invalid data: {e}\n")
            return False
         
    return True

