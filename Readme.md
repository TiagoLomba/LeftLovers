# LeftLovers
Find recipes based on the ingredients you have!

## Website
(tiagolombaa.pythonanywhere.com)

- Personalize your profile by choosing diet restricitons and foods you do not like
- Specify what type of meal you want to cook and what type of cuisine
- VOILÁ!

<!-- ### Video Demo : -->

## Instalation
- Clone / fork this repository.
- Install the required libraries listed in requirements.txt.
- Sign up to [Edamam's Recipe Search API](https://developer.edamam.com/edamam-recipe-api) to get your own API_ID and API_KEY. You can find the API documentation [here](https://developer.edamam.com/edamam-docs-recipe-api)
- Write your API_ID and API_KEY as follows:
```bash
    export API_ID="YOUR API_ID"
    export API_KEY="YOUR API_KEY"
```
- Run the application

## Technologies
--
- Flask
- Python
- SQLite
- Javascript
- jQuery
- HTML
- CSS
- Bootstrap 

## Features
### Login

Log into your account if you already have one or just press the Register Button
![App Screenshot](/static/screenshots/Screenshot1.PNG)

### Register
To register a new user into the website database, you need to write your name, username, password (and confirm it!)
![App Screenshot](/static/screenshots/Screenshot2.PNG)

### Food Restrictions

If this is your first time enterign the website or you just presses the "Select Food Restrictions" in the Menu, this is what will show up. Here you can select which cuisines you dislike and/or which Diet Restrictions you have, e.g, if you are vegetarian or pescatarian. The selected cuisine will not be displayed anymore when searching for a recipe and the added Diet Restrictions will be already added to the search. This can be changed all the time by going to the menu and clicking "Select Food Restrictions".
![App Screenshot](/static/screenshots/Screenshot3.PNG)
![App Screenshot](/static/sceenshots/Screenshot4.PNG)

### Menu

By clicking the Menu button, you have 4 options: "Select Food Restrictions" (already mentioned above); "Profile Settings" where you can change your username or password; "Log Out" (has the name suggest, you log out of your account) and "Dark Mode" so you can come to the dark side!
![App Screenshot](/static/screenshots/Screenshot5.PNG)
![App Screenshot](/static/screenshots/Screenshot7.PNG)
![App Screenshot](/static/screenshots/Screenshot8.PNG)

### Recipe Index

After you type in the ingredients and select the search parameters, the recipes will appear, displaying a picture, the calories and the time it takes to make them. You can click on a recipe you like and you will be redirected to the website so you can make it!
![App Screenshot](/static/screenshots/Screenshot6.PNG)

### Files

You will find 2 files in this repository: static and templates. The static is where you will find the images used on the site, the screenshots used in this Readme and the javascript code used throughout the site. In the templates folder you will find all the web pages available on the site. There are also python files, used to run the backend of the site.


