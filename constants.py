from colorama import Fore

MENU_HEADING_STYLE = Fore.WHITE + "----------------"

CALORIE_TRACKER_LOGO = print(Fore.BLUE + r'''
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


SPACING = {
    "THREE_SPACE" : " " * 3,
    "FIVE_SPACE" : " " * 5,
    "EIGHT_SPACE" : " " * 8,
    "TWELVE_SPACE" : " " * 12,
    "SIXTEEN_SPACE" : " " * 16,
}

class DATA_TYPE:
    TWO_MENU_ITEMS = "two_menu_items"
    THREE_MENU_ITEMS = "three_menu_items"
    FOUR_MENU_ITEMS = "four_menu_items"
    FIVE_MENU_ITEMS ="five_menu_items"
    INTEGER = "integer"
    ENTRY_NAME = "item_name"
    SEARCH_CRITERIA = "search_food_library"
    CALORIE_RANGE = "calorie_data"
    MAX_CALORIE = 3500
    MIN_CALORIES = 1500

class HEADERS:
    TRACKER_HEADERS = ["\nMeal", "\nFood Item " + SPACING["SIXTEEN_SPACE"], "Serving\nSize (g)", "\nCalories"]
    REMOVE_ITEMS_HEADER = ["Item\nNo.","\nMeal", "\nFood Item" + SPACING["SIXTEEN_SPACE"], "Serving\nSize (g)", "\nCalories"]
    SEARCH_HEADERS = ["Item\nNo.", "\nFood Item" + SPACING["SIXTEEN_SPACE"], "kCal\nper 100g"]
    CONFIRM_SEARCH_ITEM_HEADER = ["\nFood Item" + SPACING["SIXTEEN_SPACE"], "kCal\nper 100g"]
    CONFIRM_MANUAL_ITEM_HEADER = ["\nMeal", "\nName" + SPACING["SIXTEEN_SPACE"], "kCal\nper 100g", "Serving\nSize (g)"]

class MENU_ITEMS:
    ITEM_CONFIRMATION_SELECTION = ["Add Item to Tracker", "Save Item to library", "Back to Calorie Tracker"]
    SEARCH_CONFIRMATION_SELECTION = ["Add Item to Tracker", "Back to Search"]
    MEAL_TYPES =  ["Breakfast", "Lunch", "Dinner", "Snack"]
    CALORIE_TRACKER_MENU = ["Update Calorie Goal", "Manually Add Food Item", "Search & Add From Library", "Remove Item From Tracker"]

