# Libraries
import datetime
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
exercise_tracker = SHEET.worksheet("exercise_tracker")
weight_tracker = SHEET.worksheet("weight_tracker")
food_items = SHEET.worksheet("food_items")


#find_food_item =  re.compile(r"peanuts")
#food_result = food_items.findall(find_food_item)


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
    typingPrint("Loading Main Menu, Please Wait...\n".center(110))


def main():
    welcome_screen()
    menu_navigation()
    


# Concept and tutorial used from https://www.101computing.net/python-typing-text-effect/
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
  os.system("clear")

def menu_navigation():
    main_menu()
    calorie_goal_menu()
    validate_menu_data()

def main_menu():
    """
    Runs the main menu of the program.
    Allows users to navigate through program.
    """
    # Loop repeats until valid input is received
    while True:
        print()
        print(Fore.WHITE + "∙∙·▫▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒ" + Fore.BLUE + "   MAIN MENU   " + Fore.WHITE + "ₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫▫·∙∙")
        print()
        typingPrint("Please select one of the following options:\n")
        print()
        print("1. Calorie Goal")
        print("2. Calorie Tracker")
        print("3. Weight Tracker")
        print("4. Food Items")


        user_input = input("> ")
         
        # Calorie Tracker
        if user_input == "1":
            typingPrint("Loading Calorie Goal, please wait...\n".center(110))
            clearScreen()
            calorie_goal_menu()
            break

        # Exercise Tracker
        elif user_input == "2":
            typingPrint("Loading Calorie Tracker, please wait...\n".center(110))
            clearScreen()
            calorie_tracker_menu()
            break

        # Weight Tracker
        elif user_input == "3":
            typingPrint("Loading Weight Tracker, please wait...\n".center(110))
            clearScreen()
            weight_tracker_menu()
            break

        # Food Items
        elif user_input == "4":
            typingPrint("Loading Food Items, please wait...\n".center(110))
            clearScreen()
            food_items_menu()
            break

            # Invalid input raises error
        else:
            validate_menu_data("main_menu")
    
def calorie_goal_menu():
    """
    Displays calorie goal submenu
    Allows users to set a new daily calorie goal
    Navigate back to main menu
    """
    # Loop repeats until valid input is received
    while True:
        print()
        # Heading styles from https://textkool.com
        print(Fore.WHITE + "∙∙·▫▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫ₒ" + Fore.BLUE + "   CALORIE GOAL MENU   " + Fore.WHITE + "ₒ▫ᵒᴼᵒ▫ₒₒ▫ᵒᴼᵒ▫▫·∙∙")
        print()
        typingPrint("Please select one of the following options:\n")
        print()
        print("1. View Calorie Goal")
        print("2. Back to Main Menu")

        
        user_input = input("> ")

        # Update Calorie Goal
        if user_input == "1":
            typingPrint("Preparing to update, please wait...\n".center(110))
            clearScreen()
            print("Update Calorie Goal")
            break

        # Back to Main Menu
        elif user_input == "2":
            typingPrint("Loading Main Menu, please wait...\n".center(110))
            clearScreen()
            main_menu()
            break

        # Runs validation with users input
        else:
            validate_menu_data("calorie_goal_menu")
    
def validate_menu_data(current_menu):
    """
    Validates user input based on current menu
    """
    try:
        user_input = input
        call_error = ValueError()

        if current_menu == "main_menu":
            if user_input != "1" or "2" or "3" or "4":
                call_error.strerror = "Select option 1 to 4"
                raise call_error
        
        elif current_menu == "calorie_goal_menu":
            if user_input != "1" or "2":
                call_error.strerror = "Select option 1 or 2"
                raise call_error
    
    except ValueError as e:
        print()
        print(Fore.RED + f"Invalid data: {e.strerror}, please try again.\n")
         
    return True
    
       
    
    
    


def food_items_menu():
   print("Food Items")

def weight_tracker_menu():
   print("Weight Tracker")

def calorie_tracker_menu():
   print("Calorie Tracker")




main()