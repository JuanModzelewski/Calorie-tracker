# [Calorie Tracker](https://calorie-tracker-0245c5ccb0dc.herokuapp.com/)

Calorie Tacker was developed to make it simple and effective for users to manage their daily caloric intake. Calorie tracker is able to modify the calorie goal, add and remove entries, and search through a food library kept on Google Sheets. Based on the total calories of entries and the predetermined calorie goal, the remaining daily calories are calculated and displayed.



![Calorie Tracker Welcome Screen](/assets/readme-images/welcome-screen.jpg)

## User Experience (UX)
### User Goals
To help people reach their objectives more easily, the users' primary objective is to record and keep track of food items and their calorie counts. 
- The user must have the option to create new calorie goals or target.
- Since every user has a distinct dietary requirements, add custom entries to the tracker.
- To facilitate access in the future, save customized entries to a library.
- Remove items if the daily diet plan has altered or if entries are inaccurate.
- See how many calories they still have (calorie goal - total of all entries).


### User Journey
1. Welcome Screen
    - Provides a brief introduction to the application and its functions.
    - Providing the steps required to add entries and set goals

2. Calorie Tracker
    - Heading identifies the page
    - Current date is displayed above the tracker table.
    - The table gives information on the things that are presently being tracked; if there are no entries, feedback will take the place of the table section.
    - Below the table, you can see the Calorie Goal and Remaining Calorie Total.
    - Menu items give precise instructions on how to continue.

3. Update Calorie Goal
    - User is able to set a new calorie goal.
    - The user's input is verified to make sure that only numbers are submitted and that the target calorie range of 1500–3500 is reasonable.
    - The user will return to the main tracker after the calorie goal has been validated and updated in the calorie tracker.

4. Manually Add Food Items
    - Enables the user to build a custom entry in Tracker and store it in a library for convenient access to entries in the future.
    - The following steps must be followed in order to create a new entry:
        * 1. Decide on the meal schedule (breakfast, lunch, dinner, snack).
        * 2. Give the item a name and some background information.
        * 3. Type in the item's calories per 100g.
        * 4. The user will enter the item's needed serving size.
    - After the entry is previewed, you can choose to add it to the tracker, save it to the food library, or exit to main tracker.

5. Search & Add From Library
    - Allows the user to search for existing food items in the Google sheet and add food items to the tracker.
    - The following steps must be followed in order to search and add an entry:
        * 1. Type the item's name into the search field.
        * 2. If the item is found, the user has to choose it from a list by referring to the item number column.
        * 3. The chosen item will be shown for verification, with options to add it to the tracker or go back to the search.
        * 4. The user will choose their meal schedule (breakfast, lunch, supper, and snack) if they choose to add an item.
        * 5. The user will enter the item's needed serving size.
        * 6. The entry will be added to the tracker and the user will return to the Calorie Tracker

### Design
Since this is a terminal application, the interface contrast was created solely by simple text alteration and styling. Moreover, table formatting to show information in a structured table.

#### Colors
In order to create contrast and organize the information hierarchy, [Colorama](https://pypi.org/project/colorama/) was utilized to bring color to the terminal text. 
- Error messages were colored red to make error identification easier.
- Blue was used for the logo and primary elements.
- Green was used for confirmation elements and Current Calorie Goal text.
- Yellow was used for Remaining Calorie Text
- DIM was used to display information without taking focus off the main request

#### Fonts
In order to provide information hierarchy in text [Fontstyle](https://pypi.org/project/fontstyle/) with assistance from [GeeksforGeeks](https://www.geeksforgeeks.org/fontstyle-module-in-python/)
- Italic was used for information text and examples


#### Wireframe / Sketches
- This sketch was created prior to finalizing page content.
![Wireframe](/assets/images/readme-images/keyboard_hero_sketch.PNG)


## Existing Features

### Welcome Screen

![Welcome Screen](/assets/readme-images/welcome-screen.jpg)

- 

### Main Calorie Tracker
| Screen | Image |
| :---         |          ---: |
| 1. Calorie Tracker without entries| ![No Entries](/assets/readme-images/calorie-tracker-main-no-entries.jpg) |
| 2. Calorie Tracker with entries | ![With Entries](/assets/readme-images/calorie-tracker-main-with-new%20entry.jpg) |

- Shows entries if any are found for the current day; if not, placeholder text will take the place of the table.
- Displays Current Calorie Goal and Remaining Calories below the table.
- Offers menu options that the user can select from based on the require outcome
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

- Entry is then added to the Tracker and user is returned to the Calorie Tracker

### Remove Item From Tracker

- Remove any currently tracked items from the Calorie Tracker

![Remove Tracked Items](/assets/readme-images/remove-entries.jpg)

- Select the Item No. in the first colum corresponding to the entry that is to be removed.
- The user can return to the Calorie Tracker by typing "exit"

## Technologies Used

### Languages

- [Python3](https://en.wikipedia.org/wiki/Python_(programming_language))

Provided as part of Code Institute's [Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template): 

### Frameworks, Libraries, and Packages

- [Colorama](https://pypi.org/project/colorama/) was used to add colour to the terminal.

- [Datetime](https://docs.python.org/3/library/datetime.html) was used to validate date inputs.

- [GitHub](https://github.com/) was used to store the project and for version control.

- [GitHub (GitHub Desktop):](https://github.com/)
    GitHub is used to store the project's code after being pushed from Git.
    GitHub Desktop allows for easy creation and storing of repositories locally and an alternative push method.

- [VS Code:](https://code.visualstudio.com/) Visual Studio Code was used as IDE.

- [GSpread](https://docs.gspread.org/en/v6.0.0/) was used to interact with the data in the linked sheet.

- [Google OAuth](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html) was used to authenticate the program in order to access Google's APIs.

- [Google Cloud](https://cloud.google.com/) was used to generate the APIs required to connect the data sheets with the Python code.

- [Google Sheets](https://docs.google.com/spreadsheets/) was used to store user input data.

- [Heroku](https://dashboard.heroku.com/login) was used to host and deploy the finished project.

- [Lucidchart](https://www.lucidchart.com/pages/) was used to create the flowchart during project planning.

- [Many Tools](https://manytools.org/hacker-tools/ascii-banner/) was used to create a logo for the program.

- [Os](https://docs.python.org/3/library/os.html) was used to clear the screen when switching between menus or views. 

- [Sys](https://docs.python.org/3/library/sys.html) was used to create the menu loading style

- [Tabulate](https://pypi.org/project/tabulate/) was used to display tables in Calorie Tracker, Remove Items Table, Item Confirmation Table, Search Table

- [Time](https://docs.python.org/3/library/time.html) . 

<br>
<br>

## Testing


### Manual Testing Features

#### Welcome Screen
| Feature | Expected Outcome | Result |
| :---         |     :---      |          :---: |
| Page Load | Welcome screen loads displaying welcome message and information on application use | Pass |
| Input Enter to continue | When Enter is pressed the application loads the calorie tracker  | Pass |
| Loading Animation | The Loading bar is displayed with the correct loading text  | Pass |

#### Calorie Tracker
| Feature | Expected Outcome | Result |
| :---         |     :---      |          :---: |
| Page Load | The Calorie Tracker loads with heading, current date, tracker table if present, calorie goal with remaining calories and menu options | Pass |
| Menu Heading | Menu Heading is clearly displayed with the correct title | Pass |
| Correct Date Inserted | The Table Date is displayed with the correct date information  | Pass |
| Calorie Table | Table entries are correctly displayed in the Tracker table, place holder text is present if there are no tracked entries | Pass |
| Calorie Goal | The correct Calorie Goal is displayed below the table | Pass |
| Remaining Calories | Remaining Calories are correctly calculated and displayed below the table | Pass |
| Menu Selection | Menu Items are present and in the correct order | Pass |
| Loading Animation | The Loading bar is displayed with the correct loading text based on menu option selected  | Pass |


#### Update Calorie Goal
| Feature | Expected Outcome | Result |
| :---         |     :---      |          :---: |
| Page Load | Calorie Goal page loads and request is displayed | Pass |
| Menu Heading | Menu Heading is clearly displayed with the correct title | Pass |
| Update Calorie Goal | If the correct input is entered the new Calorie Goal is added to the tracker | Pass |
| Loading Animation | The Loading bar is displayed with the correct loading text | Pass |
| Calorie Tracker Loaded | The Calorie Tracker is loaded and the new calorie goal is displayed | Pass |


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

### Validator Testing 


### Bugs
No bugs to report


## Deployment
The program was developed using GitPod, which was then committed and pushed to GitHub using the GitPod terminal. The finished project was deployed in Heroku using the Code Institute Python Terminal for display purposes.

### Connecting Google Sheets
- This project required the use of Google Drive API and Google Sheets API, both enabled via Google Cloud Platform.
- A credentials file was generated through the Google Drive API and added to the workspace.
- To ensure that the sensitive information contained in the credentials would not be pushed to the repository, the credentials file was added to gitignore.
- The client_email address contained within the credentials file was added to Google Sheets as an editor to enable access.
- Variables and scope to access the worksheet were defined at the top of the run.py file.
- Using the terminal, GSpread and OAuth packages were installed.

### Heroku
Deployment to Heroku was completed using the following steps:

1. Update your requirements.txt file
    - Run pip3 freeze > requirements.txt' in the terminal to add a list of dependencies to requirements.txt.
    - Commit and push the changes to Github.
2. Log in to Heroku and from the dashboard, click Create New App.
    - Enter an app name and choose your region. Click Create App.
3. Go to Settings and update the ConfigVars.
    - Click Reveal ConfigVars and add the following information:
        - KEY = 'CREDS', VALUE = Copy and paste the entire contents of the creds.json file into this field.
        - KEY = 'PORT', VALUE = '8000'.
    - Click Add after entering each ConfigVar.
4. Within Settings, update the Buildpacks.
    - Click Add Buildpack and add the following buildpacks:
        - Add Python and click Add Buildpack.
        - Add NodeJS and click Add Buildpack.
        - Make sure the Python buildpack is above the NodeJS buildpack.
5. Go to Deploy and specify deployment details.
    - Select GitHub as the Deployment Method.
        - When prompted to Connect to GitHub, find your repository and click Connect.
    - Select either Automatic Deploys or Manual Deploys and click Deploy Branch.
6. Once deployment has been completed, click View to view the deployed project.

- The live link is [KeyBoard Hero](https://calorie-tracker-0245c5ccb0dc.herokuapp.com/)

## Credits

### Content

- Code


### Media



https://gfitnessonline.com/calorie-tracker-spreadsheet/
