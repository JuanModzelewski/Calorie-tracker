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

    # Intro to explain program purpose 
    print("Welcome to Calorie Tracker.\n")


def main():
    welcome_screen()


main()