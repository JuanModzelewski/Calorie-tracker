import os
from colorama import Back, Fore
import sys
import time

class DATA_TYPE:
    TWO_MENU_ITEMS = "two_menu_items"
    THREE_MENU_ITEMS = "three_menu_items"
    FOUR_MENU_ITEMS = "four_menu_items"
    FIVE_MENU_ITEMS ="five_menu_items"
    INTEGER = "integer"
    ENTRY_NAME = "item_name"
    SEARCH_CRITERIA = "search_food_library"
    CALORIE_RANGE = "calorie_data"

MENU_HEADING_STYLE = Fore.WHITE + "----------------"
THREE_SPACE = " " * 3
FIVE_SPACE = " " * 5
EIGHT_SPACE = " " * 8
TWELVE_SPACE = " " * 12
SIXTEEN_SPACE = " " * 16


def loading_style(text, text_color = Fore.BLACK, background_color = Back.WHITE):
    for character in text:
        sys.stdout.write(text_color + background_color + character)
        sys.stdout.flush()
        time.sleep(0.01)

def typing_print(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.02)

def pause_clear():
    """
    Clears screen after a brief pause.
    """
    time.sleep(1.5)
    clear_screen()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[2J')

def menu_headings(title):
    print(f"{MENU_HEADING_STYLE}  {title}  {MENU_HEADING_STYLE}".center(70))
    print()

def request(text):
    print(THREE_SPACE + text)
    print()

def loading_menu(text):
        print()
        loading_style(f"{EIGHT_SPACE} {text}, PLEASE WAIT {EIGHT_SPACE}".center(70), Fore.GREEN, Back.BLACK)
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
            if not 1500 <= int(value) <= 3500:
                raise ValueError("Select a goal between 1500 and 3500")
        
        elif data == DATA_TYPE.INTEGER:
            if not int(value):
                raise ValueError("You can only enter numbers")
               
        # Validates string length for item added to tracker and library    
        elif data == DATA_TYPE.ENTRY_NAME:
            if not value != "" or len(value) > 50 :
                raise ValueError("Category must be between 0 and 50 characters") 

        # Search criteria must be 3 characters or more
        elif data == DATA_TYPE.SEARCH_CRITERIA:
            if len(value) < 3:
                raise ValueError("A minimum of 3 characters required")
            
    except ValueError as e:
            print()
            print(Fore.RED + THREE_SPACE + f"Invalid data: {e}\n")
            return False
         
    return True

