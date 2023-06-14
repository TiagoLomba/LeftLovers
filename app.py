import json

from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, time_now, database_connect, stringify, lookup

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#API
APP_ID = "89232447"
API_KEY = "ab5a8b2af43c8532c5c061cc41da06dd"
# # Make sure API_KEY and API_ID are set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")
# elif not os.environ.get("API_ID"):
#     raise RuntimeError("API_ID not set")
URL = f'https://api.edamam.com/api/recipes/v2?type=public&app_id={APP_ID}&app_key={API_KEY}/'


#Dictionaries ####
cuisineType = {
    "chinese": "Chinese",
    "eastern europe": "Eastern Europe",
    "british": "British",
    "caribbean": "Caribbean",
    "asian": "Asian",
    "central europe": "Central Europe",
    "american": "American",
    "french": "French",
    "kosher": "Kosher",
    "indian": "Indian",
    "korean": "Korean",
    "italian": "Italian",
    "greek": "Greek",
    "japanese": "Japanese",
    "mediterranean": "Mediterranean",
    "south east asian": "South East Asian",
    "mexican": "Mexican",
    "south american": "South American",
    "world": "World",
    "nordic": "Nordic",
    "middle eastern": "Middle Eastern",
}


dishType = {
    "starter": "Starter",
    "main course": "Main Course",
    "side dish": "Side Dish",
    "drinks": "Drinks",
    "desserts": "Desserts",
}

health = {
    "pescatarian": "Pescatarian",
    "shellfish-free": "Shellfish-Free",
    "alcohol-free": "Alcohol-Free",
    "celery-free": "Celery-Free",
    "soy-free": "Soy-Free",
    "sugar-free": "Sugar-Free",
    "pork-free": "Pork-Free",
    "red-meat-free": "Red-Meat-Free",
    "sesame-free": "Sesame-Free",
    "sulfite-free": "Sulfite-Free",
    "tree-nut-free": "Tree-Nut-Free",
    "vegan": "Vegan",
    "sugar-conscious": "Sugar-Conscious",
    "vegetarian": "Vegetarian",
    "wheat-free": "Wheat-Free",
    "alcohol-cocktail": "Alcohol-Cocktail",
    "crustacean-free": "Crustacean-Free",
    "dairy-free": "Dairy-Free",
    "lupine-free": "Lupine-Free",
    "mediterranean": "Mediterranean",
    "dash": "DASH",
    "kidney-friendly": "Kidney-Friendly",
    "egg-free": "Egg-Free",
    "fish-free": "Fish-Free",
    "fodmap-free": "FODMAP-Free",
    "gluten-free": "Gluten-Free",
    "mollusk-free": "Mollusk-Free",
    "peanut-free": "Peanut-Free",
    "immuno-supportive": "Immuno-Supportive",
    "keto-friendly": "Keto-Friendly",
    "low-sugar": "Low-Sugar",
    "mustard-free": "Mustard-Free",
    "kosher": "Kosher",
    "low-potassium": "Low-Potassium",
    "no-oil-added": "No oil added",
    "paleo": "Paleo",
}
############

# Create user table if it does not exist already
def create_user_table():
    con, cur = database_connect()
    cur.execute("""
     CREATE TABLE IF NOT EXISTS users (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         username TEXT NOT NULL,
         hash TEXT NOT NULL,
         cuisineType TEXT,
         healthType TEXT,
         lastLogIn TEXT
     )
 """)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
        name = session["name"]
        user_id = session["user_id"]
        con, cur = database_connect()
        user_data = cur.execute("SELECT cuisineType, healthType FROM users WHERE id=?", (user_id,))
        user_data = cur.fetchone()
        con.close()
        if user_data[0] is not None and user_data[1] is not None:
            #Parse JSON strings and convert them into python dictionaries
            cuisine_types = json.loads(user_data[0])
            health_types = json.loads(user_data[1])
            print("/n HealthTypes: ", health_types)
            #Only show the available options
            available_health = {key: value for key, value in health.items() if key not in health_types}
            return render_template("index.html", cuisineType=cuisine_types, dishType=dishType, health=health_types, available_health=available_health, name=name)
        else:
            available_health = {key: value for key, value in health.items()}
            return render_template("index.html", cuisineType=cuisineType, dishType=dishType, health={}, available_health=available_health, name=name)


@app.route("/get_available_health", methods=["GET"])
@login_required
def get_available_health():
    user_id = session["user_id"]
    con, cur = database_connect()
    user_data = cur.execute("SELECT healthType FROM users WHERE id=?", (user_id,))
    user_data = user_data.fetchone()
    con.close()

    if user_data:
        health_types = json.loads(user_data[0])
        available_health = {key: value for key, value in health.items() if key not in health_types}
        return jsonify(available_health=list(available_health.values()))
    else:
        return jsonify(available_health=[])


@app.route("/recipe_index", methods=["GET", "POST"])
@login_required
def recipe_index():
    name = session["name"]
    if request.method == "POST":
        next = request.form.get("nextPageLink")
        if next:
            nextPage = True
            recipes_list = lookup(next, nextPage)
            i_list = request.form.getlist("ingredients")
            ingredients = " ".join(i_list)
            return render_template("recipe_index.html", ingredients=ingredients, recipes_list=recipes_list[0], nextPageLink=recipes_list[1], name=name)
        else:   
            i_list = request.form.getlist("ingredients")
            ingredients = " ".join(i_list)
            # print(ingredients)
            
            #Get Selected info from the index form
            cuisine_list = stringify("cuisineType","&cuisineType=")
            health_list = stringify("health_labels", "&health=")
            dish_list = stringify("dishType","&dishType=")

            query = "".join(ingredients + health_list + cuisine_list + dish_list)
            nextPage = False
            recipes_list = lookup(query, nextPage)
            return render_template("recipe_index.html", ingredients=ingredients, recipes_list=recipes_list[0], nextPageLink=recipes_list[1], name=name)
    else:
        return redirect("/")


@app.route("/restrictions", methods=["GET", "POST"])
@login_required
def restrictions():
    name = session["name"]
    user_id = session["user_id"]
    if request.method == "POST":
        data = request.get_json()
        selected_cuisines = data['cuisineType']
        selected_health = data['health']

        available_cuisine_type = {key: value for key, value in cuisineType.items() if key not in selected_cuisines}
        health_options = {key: value for key, value in health.items() if key in selected_health}

        cuisineType_json = json.dumps(available_cuisine_type)
        health_json=json.dumps(health_options)

        con, cur = database_connect()
        cur.execute('UPDATE users SET cuisineType=?, healthType=? WHERE id=?', (cuisineType_json, health_json, user_id))
        con.commit()
        con.close()
        return redirect("/")

    else:
        return render_template("restrictions.html", cuisineType = cuisineType, health=health, name=name)


@app.route("/login", methods = ["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            errorMessage = "Please insert a valid username and/or password!"
            return render_template("login.html", errorMessage = errorMessage)

        con, cur = database_connect()
        user_db = cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_db = user_db.fetchall()

        # Ensure username exists and password is correct
        if len(user_db) != 1 or not check_password_hash(user_db[0][3], request.form.get("password")):
            errorMessage = "Invalid username and/or password!"
            return render_template("login.html", errorMessage = errorMessage)

        # Remember which user has logged in
        session["user_id"] = user_db[0][0]
        session["name"] = user_db[0][1]

        #Check if it the first time the user logs in
        lastLogIn = cur.execute("SELECT lastLogIn FROM users WHERE id = ?", (session["user_id"],))
        lastLogIn = lastLogIn.fetchone()

        if lastLogIn[0] is None:
            lastLogIn = time_now()
            cur.execute("UPDATE users SET lastLogIn = ? WHERE id = ?", (lastLogIn, session["user_id"]))
            con.commit()
            con.close()
            return redirect("/restrictions")
        else:
            lastLogIn = time_now()
            cur.execute("UPDATE users SET lastLogIn = ? WHERE id = ?", (lastLogIn, session["user_id"]))
            con.commit()
            con.close() 
            return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        passwordConfirmation = request.form.get("passwordConfirmation")

        con, cur = database_connect()
        #Error Handle
        if not name:
            errorMessage = "Please insert your name"
            return render_template("register.html", errorMessage=errorMessage)
        if not username or not password or not passwordConfirmation:
            errorMessage = "Please insert a valid username and/or password"
            return render_template("register.html", errorMessage=errorMessage)
        elif len(password) <  6:
            errorMessage = "Password is too short"
            return render_template("register.html", errorMessage=errorMessage)
        elif password != passwordConfirmation:
            errorMessage = "Passwords do not match!"
            return render_template("register.html", errorMessage=errorMessage)
        elif cur.execute("SELECT * FROM users WHERE username = ?", (username)).fetchone() is not None:
            errorMessage = "Username already registered"
            return render_template("register.html", errorMessage=errorMessage)
        

        #Add user to database
        cur.execute("INSERT INTO users (name, username, hash) VALUES (?,?,?)", (name, username, generate_password_hash(password)))
        con.commit()
        con.close()
        flash("Registered Successfully!")
        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    name = session["name"]

    if request.method == "POST":
        user_id = session["user_id"]
        currentPassword = request.form.get("currentPassword")
        newPassword = request.form.get("newPassword")
        newUsername = request.form.get("newUsername")
        con, cur = database_connect()
        currentUsername = cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        currentUsername = currentUsername.fetchone()

        user_db = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_db = user_db.fetchall()
        

        if not newPassword and not currentPassword:
            if newUsername == currentUsername:
                 errorMessage = "That is already your username!"
                 con.close()
                 return render_template("settings.html", errorMessage = errorMessage)
            else:
                cur.execute("UPDATE users SET username=? WHERE id=?", (newUsername, user_id))
                con.commit()
                con.close()
                flash("Username Updated!")
            return redirect("/settings")
        if not check_password_hash(user_db[0][3], request.form.get("currentPassword")):
            errorMessage = "That is not your current password!"
            return render_template("settings.html", errorMessage = errorMessage)
        else:
            cur.execute("UPDATE users SET hash = ? WHERE id = ?", (generate_password_hash(newPassword), user_id))
            con.commit()
            con.close()
            flash("Password Updated!")
            return redirect("/settings")

    else:
        return render_template("settings.html", name=name)
    
if __name__ == "__main__":
    create_user_table()  # Set database if it does not exist
    app.run()
