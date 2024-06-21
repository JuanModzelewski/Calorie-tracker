# [Calorie Tracker](https://calorie-tracker-0245c5ccb0dc.herokuapp.com/)

Calorie Tacker was developed to make it simple and effective for users to manage their daily caloric intake. Calorie tracker is able to modify the calorie goal, add and remove entries, and search through a food library kept on Google Sheets. Based on the total calories of entries and the predetermined calorie goal, the remaining daily calories are calculated and displayed.



![Calorie Tracker Welcome Screen](/assets/readme-images/welcome-screen.jpg)

## User Experience (UX)
### User Goals
To help people reach their objectives more easily, the users' primary objective is to record and keep track of food items and their calorie counts. 
- The user must have the option to update the calorie goals to match their calorie target.
- Since every user has a distinct dietary requirements, the ability to add custom entries to the tracker is present.
- To facilitate access to food items in the future, the user is able to save customized entries to the food library.
- Providing a means to remove items if the daily diet plan has altered or if entries are inaccurate.
- Displaying how many calories the user still has before reaching the daily target, provides visual feedback (calorie goal - total of all entries).


### User Journey
1. Welcome Screen
    - Provides a brief introduction to the application and its functions.
    - Displaying key functions and understanding to get the user started on their calorie tracking experience.

2. Calorie Tracker
    - Heading clearly identifies the current page.
    - Current date is displayed above the tracker table along side the table title, Currently Tracked Items.
    - The table provides information on the items that are presently being tracked; if there are no entries, feedback will take the place of the table section.
    - Remaining Calories for the day, are displayed and adapted as entries are added providing the user with visual feedback.
    - Menu items give precise instructions on how to continue.

3. Update Calorie Goal
    - User is able to set a new calorie goal based on their requirements.
    - The user's input is verified to make sure that only numbers are submitted and that the target calorie range of 1500–3500 is reasonable.
    - The user will return to the Calorie Tracker after the calorie goal has been validated and updated.

4. Manually Add Food Items
    - This enables the user to build a custom entry in Tracker and store it in a library for convenient access to entries in the future.
    - The following steps must be followed in order to create a new entry:
        1. Decide on the meal schedule (breakfast, lunch, dinner, snack).
        2. Give the item a name and some background information.
        3. Enter the item's calories per 100g.
        4. The user will enter the item's needed serving size.
        5. Preview and confirm entry information and choose from displayed options.
            - The user can choose to add the entry to the tracker, save the item to the food library, or exit to main tracker.

5. Search & Add From Library
    - Allows the user to search for existing food items in the Google sheet Food Library and add items to the tracker.
    - The following steps must be followed in order to search and add an entry:
        1. Type the item's name into the search field.
        2. If the item is found, the user has to choose an option from a results table by referring to the item number column.
        3. The chosen item will be shown for verification, with options to add it to the tracker or go back to the search.
        4. The user will choose their meal schedule (breakfast, lunch, supper, and snack) if they choose to add an item.
        5. The user will enter the item's needed serving size.
        6. The entry will be added to the tracker and the user will return to the Calorie Tracker
<br>
<br>

## Design
Since this is a terminal application, the interface contrast was created solely by simple text alteration and styling using [Colorama](https://pypi.org/project/colorama/).
Adding data into a table format using [Tabulate](https://pypi.org/project/tabulate/) provides a clean and structure approach to displaying information.

### Colors
In order to create contrast and organize the information hierarchy, [Colorama](https://pypi.org/project/colorama/) was utilized to bring color to the terminal text. 
- Error messages are colored red to make error identification easier.
- Blue was used for the logo and primary elements.
- Green was used for confirmation elements and Current Calorie Goal text.
- Yellow was used for Remaining Calorie Text
- DIM was used to display information without taking focus off the main request

### Fonts
In order to provide information hierarchy with text [Fontstyle](https://pypi.org/project/fontstyle/) was used. Assistance from [GeeksforGeeks](https://www.geeksforgeeks.org/fontstyle-module-in-python/)
- Italic was used for information text and examples
- Bold was used for main requests and headings
<br>
<br>

## Existing Features
### Welcome Screen

![Welcome Screen](/assets/readme-images/welcome-screen.jpg)

- Provides the user with the primary functionality of Calorie tracker and basic information to get started with tracking entries. 

### Main Calorie Tracker
| Screen | Image |
| :---         |          :--- |
| 1. Calorie Tracker without entries| ![No Entries](/assets/readme-images/calorie-tracker-main-no-entries.jpg) |
| 2. Calorie Tracker with entries | ![With Entries](/assets/readme-images/calorie-tracker-main-with-new%20entry.jpg) |

- Displays entries if any are found for the current day; if not, placeholder text will take the place of the table.
- The Current Calorie Goal and Remaining Calories for the day are displayed below the table.
- Menu options are presented that the user can select from based on the require outcome
 - Update Calorie Goal
 - Manually Add Food Item
 - Search & Add From Library
 - Remove Items From Tracker

### Update Calorie Goal

![Update Calorie Goal](/assets/readme-images/change-calorie-goal.jpg)

- Allows the user to modify the calorie target in accordance with their dietary needs and desired goals


### Manually Add Food Item

- Allows for the addition of a new entry to the Calorie Tracker. The following screen and processes are described:

| Step | Image |
| :---         |          :--- |
| 1. Select the Meal Schedule | ![Entry Meal](/assets/readme-images/meal-selection.jpg) |
| 2. Provide a Name for Food Item | ![Item Name](/assets/readme-images/item-name.jpg) |
| 3. Enter the amount of Calories (kCal) per 100g | ![Item Calories](/assets/readme-images/item-calories-info.jpg) |
| 4. Enter the desired serving size of Item | ![Item Name](/assets/readme-images/item-serving-size.jpg) |
| 5. Confirm Entry and Choose to Add to Tracker or Save to Library | ![Item Confirmation](/assets/readme-images/item-confirmation-manual-add.jpg) |

- Add Item to Tracker (Adds Entry to Tracker and returns User to Calorie Tracker)
- Save Item to Library (Save the entry to the Food Library)
- Exit to Calorie Tracker (Returns the user to Calorie Tracker)

### Search & Add From Library

- Items found in the library can be searched through and added to the calorie tracker. The following screen and processes are described:

| Step | Image |
| :---         |          :--- |
| 1. Enter the item you want to look for | ![Search Food Library](/assets/readme-images/search-food-library.jpg) |
| 2. Select an Item from the search results | ![Search Results](/assets/readme-images/search-result-selection.jpg) |
| 3. Confirm the selected item | ![Search Confirmation](/assets/readme-images/search-item-confirmation.jpg) |
| 4. Select the Meal Schedule | ![Entry Meal](/assets/readme-images/meal-selection.jpg) |
| 5. Enter the desired serving size of Item | ![Item Name](/assets/readme-images/item-serving-size.jpg) |

- The entry is then added to the Tracker and the user is returned to the Calorie Tracker

### Remove Item From Tracker

- Remove any currently tracked items from the Calorie Tracker

![Remove Tracked Items](/assets/readme-images/remove-entries.jpg)

- Select the Item No. in the first colum corresponding to the entry that is to be removed.
- The user can return to the Calorie Tracker by typing "exit"
<br>
<br>

## Technologies Used

### Languages

- [Python3](https://www.python.org/downloads/)

- Template provided by Code Institute [Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template): 

### Frameworks, Libraries, and Packages

- [Colorama](https://pypi.org/project/colorama/) used to add text color to the terminal and create information hierarchy and add contrast.
- [Datetime](https://docs.python.org/3/library/datetime.html) used to find and display entries for the current day.
- [GitHub](https://github.com/) used to store the project and for version control.
- [GitHub (GitHub Desktop):](https://github.com/) allows for easy creation and storing of repositories locally and provides an alternative push method.
- [VS Code:](https://code.visualstudio.com/) was the primary IDE.
- [GSpread](https://docs.gspread.org/en/v6.0.0/) used to interact with the data on linked sheets.
- [Google OAuth](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html) used to authenticate the program in order to access Google's APIs.
- [Google Cloud](https://cloud.google.com/) used to generate the APIs required to connect the data sheets with the Python code.
- [Google Sheets](https://docs.google.com/spreadsheets/) used to store tracked entries, calorie goal and food library.
- [Heroku](https://dashboard.heroku.com/login) used to host and deploy the complete project.
- [Many Tools](https://manytools.org/hacker-tools/ascii-banner/) used to create the Calorie Tracker logo.
- [Os](https://docs.python.org/3/library/os.html) used to clear the screen when switching between menus or user inputs
- [Sys](https://docs.python.org/3/library/sys.html) used to create the menu loading style
- [Tabulate](https://pypi.org/project/tabulate/) used to display all application tables, Calorie Tracker, Remove Items Table, Item Confirmation Table, Search Table
- [Time](https://docs.python.org/3/library/time.html) used to briefly pause the screen before loading the next pages content. 
<br>
<br>

## Testing
### Manual Testing Features
#### Welcome Screen
| Feature | Expected Outcome | Result |
| :---         |     :---      |          :---: |
| Page Loads | Welcome screen loads displaying welcome message and information on application use | Pass |
| Input Enter to continue | When 'return' is pressed the Calorie Tracker is loaded  | Pass |
| Loading Animation | The Loading bar is displayed with the correct loading text  | Pass |


#### Calorie Tracker
| Feature | Expected Outcome | Result |
| :---         |     :---      |          :---: |
| Page Loads | The Calorie Tracker loads with the page heading, table heading with current date, tracker table if present, calorie goal with remaining calories and menu selection options | Pass |
| Menu Heading | Menu Heading is clearly displayed with the correct title | Pass |
| Correct Date Displayed | The Table Date is displayed with the correct date information set to current date | Pass |
| Calorie Tracker Table | Table entries are correctly displayed in the Tracker table, place holder text is present if there are no tracked entries | Pass |
| Calorie Goal | The correct Calorie Goal is displayed below the table in green text | Pass |
| Remaining Calories | Remaining Calories are correctly calculated and displayed in yellow text below the table along side Calorie Goal | Pass |
| Menu Selection | Menu Items are present and in the correct order | Pass |
| Loading Animation | The Loading bar is displayed with the correct loading text based on menu option selected | Pass |


#### Update Calorie Goal
| Feature | Expected Outcome | Result |
| :---         |     :---      |          :---: |
| Page Loads | Calorie Goal page loads and request is displayed to enter new Calorie Goal | Pass |
| Menu Heading | Menu Heading is clearly displayed with the correct title | Pass |
| Update Calorie Goal | If the correct input is entered the new Calorie Goal is added to the tracker | Pass |
| Loading Animation | The Loading bar is displayed with the correct loading text | Pass |
| Calorie Tracker Loads | The Calorie Tracker is loaded and the new calorie goal is displayed | Pass |


#### Manually Add Food Item
| Feature | Expected Outcome | Result |
| :---         |     :---     |          :---: |
| Item Meal Selection | Page loads displaying the correct meal options to be selected | Pass |
| Item Name | Page loads and request to enter Item Name is given with an example of the format to be used | Pass |
| Enter the amount of Calories (kCal) per 100g | Page loads with request and information on where to find the items calories per 100g | Pass |
| Enter the desired serving size of Item | Page loads with request to enter the desired serving size for the item | Pass |
| Entry confirmation | Page loads displaying a preview of the created entry and providing options to proceed | Pass |
| Save Item to Library | Item is added to the library and confirmation screen displayed again | Pass |
| Add Item to Tracker | Entry is added to the tracker and the Calorie Tracker is displayed | Pass |


#### Search & Add From Library
| Feature | Expected Outcome | Result |
| :---         |     :---     |          :---: |
| Page Loads | Search Food Library page loads and request is displayed to enter the food item to search for | Pass |
| Menu Heading | Menu Heading is clearly displayed with the correct title | Pass |
| Select Available Option | Any item found in search are displayed in a table and corresponding Item No. can be entered to select an item | Pass |
| Confirm Selected Item | Page loads with preview to confirm selected item and menu options to Add Item to Tracker or Back To Search | Pass |
| Item Meal Selection | Page loads displaying the correct meal options to be selected | Pass |
| Enter the desired serving size of Item | Page loads with request to enter the desired serving size for the item | Pass |
| Loading Animation | The Loading bar is displayed with the correct loading text | Pass |
| Calorie Tracker Loads | The Calorie Tracker is loaded with the new item being displayed in the Tracker table | Pass |


#### Search & Add From Library
| Feature | Expected Outcome | Result |
| :---         |     :---     |          :---: |
| Page Loads | Remove Items page loads displaying currently tracked items table and request to select a number from Item No. Colum to remove corresponding Food Entry | Pass |
| Menu Heading | Menu Heading is clearly displayed with the correct title | Pass |
| Item No. Selected | Item No. is selected and loading Animation begins | Pass |
| Loading Animation | The Loading bar is displayed with the correct loading text | Pass |
| Remove Items Page | Remove Items page loads with the selected item removed from the table | Pass |
| Exit to Calorie Tracker | Type 'exit' to return to the Calorie Tracker | Pass |


### Input Validation Testing
| Input | Validation | Error Message | Result |
| :---         |     :---     |          :--- |          :---: |
| Calorie Tracker Options | Checks if options 1 to 4 has been selected | Invalid data: Select option 1 to 4 | Pass |
| Calorie Goal Input | Checks if input is between 1500 and 3500 | Invalid data: Select a goal between 1500 and 3500 | Pass |
| Calorie Goal Input | Checks if input is an number | Invalid data: invalid literal for int() with base 10: '' | Pass |
| Item Meal | Checks if options 1 to 4 has been selected | Invalid data: Select option 1 to 4 | Pass |
| Item Name | Checks if user input is between 5 and 50 character | Invalid data: Item Name must be between 5 and 50 characters | Pass |
| Item Calories | Checks if input is an number | Invalid data: invalid literal for int() with base 10: '' | Pass |
| Serving Size | Checks if input is an number | Invalid data: invalid literal for int() with base 10: '' | Pass |
| Confirm Manual Entry | Checks if options 1 to 3 has been selected | Invalid data: Select option 1 to 3 | Pass |
| Search Food Library | Checks if user input is greater than three characters | Invalid data: Select option 1 to 3 | Pass |
| Search Food Library | If search item could not be found | There are no items matching your search criteria | Pass |
| Search Item Selection | Checks to see if the item in Food Item colum exits if not an error is displayed | Invalid data: Select a number from the first colum | Pass |
| Search Confirmation | Checks if options 1 to 2 has been selected | Invalid data: Select option 1 to 2 | Pass |
| Remove Item Menu | Checks to see if the food item in Item no. colum exits if not an error is displayed | Invalid data: Select a number from the Item No. colum | Pass |

### CI Python Linter

Passed with no errors found
![CI Python Linter Results](/assets/readme-images/ci-python-linter-results.jpg)

### Bugs
No bugs to report
<br>
<br>

## Deployment
The application was created in Visual Studio, using the CI love sandwiches template. All commits and push requests were done through the VS Code terminal. The application was deployed in Heroku using instructions from the CI love sandwiches project as reference. 

### Connecting Google Sheets
- This project required the use of Google Drive API and Google Sheets API, both enabled via Google Cloud Platform.
- A credentials file was generated through the Google Drive API and added to the workspace.
- To ensure that the sensitive information contained in the credentials would not be pushed to the repository, the credentials file was added to gitignore.
- The client_email address contained within the credentials file was added to Google Sheets as an editor to enable access.
- Variables and scope to access the worksheet were defined at the top of the run.py file.
- Using the terminal, GSpread and OAuth packages were installed.

### Heroku
Deployment to Heroku was completed using the following steps:

1. Update your requirements.txt file by entering entering the below into the terminal:
    - Run pip3 freeze > requirements.txt'.
    - Commit and push the changes to Github.
2. Log in to Heroku and select New / Create new app.
    - Create an app name and select your region. 
    - Click Create App to continue.
3. Navigate to the Settings tab locate the ConfigVars section.
    - Click Reveal ConfigVars and add the following information:
     - KEY = 'CREDS', VALUE = Copy and paste the entire contents of the creds.json file into this field.
    - KEY = 'PORT', VALUE = '8000'.
    - Click Add after entering each ConfigVar.
4. Within Settings, locate Buildpacks section.
    - Click Add Buildpack and add the following buildpacks:
    - Add Python and click Add Buildpack.
    - Add NodeJS and click Add Buildpack.
    - Make sure the Python buildpack is above the NodeJS buildpack.
5. Go to Deploy tab and complete the deployment details.
    - Select GitHub as the Deployment Method.
    - Connect to GitHub and locate your repository and select Connect.
    - Select either to Automatic Deploy or Manual Deploy your and click Deploy Branch.
6. Once deployed, select open app to view the deployed project.

- The live link is [Calorie Tracker](https://calorie-tracker-0245c5ccb0dc.herokuapp.com/)

## Credits

### Content

- Code


### Media



https://gfitnessonline.com/calorie-tracker-spreadsheet/
