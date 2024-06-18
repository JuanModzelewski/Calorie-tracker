import os
from colorama import Back, Fore
import sys
import time
from constants import DATA_TYPE, SPACING, MENU_HEADING_STYLE



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
    print(SPACING.THREE_SPACE + text)

def loading_menu(text):
        print()
        loading_style(f"{SPACING.EIGHT_SPACE} {text}, PLEASE WAIT {SPACING.EIGHT_SPACE}".center(70), Fore.GREEN, Back.BLACK)
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
            if not value != "" or len(value) > 50 :
                raise ValueError("Item Name must be between 0 and 50 characters") 

        # Search criteria must be 3 characters or more
        elif data == DATA_TYPE.SEARCH_CRITERIA:
            if len(value) < 3:
                raise ValueError("A minimum of 3 characters required")
            
    except ValueError as e:
            print()
            print(Fore.RED + SPACING.THREE_SPACE + f"Invalid data: {e}\n")
            return False
         
    return True

