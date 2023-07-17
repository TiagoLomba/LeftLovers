import requests
import json
import sqlite3

from flask import redirect, render_template, request, session
from functools import wraps
from os import path

from datetime import datetime, timezone

ROOT = path.dirname(path.realpath(__file__))

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function




def time_now():
    """get current UTC date and time"""
    now_utc = datetime.now(timezone.utc)
    return str(now_utc.date()) + ' @time ' + now_utc.time().strftime("%H:%M:%S")


def database_connect(db=path.join(ROOT, "leflovers.db")):
    con = sqlite3.connect(db)
    cur = con.cursor()
    return con, cur

def stringify(typeList, string):
    list = request.form.getlist(typeList)
    lq=[]

    if typeList == "health_labels":
        con, cur = database_connect()
        healthType = cur.execute("SELECT healthType FROM users WHERE id = ?", (session["user_id"],))
        healthType = cur.fetchone()
        health_restrictions = json.loads(healthType[0]) 
        con.close()
        if health_restrictions:
            for restriction in health_restrictions.values():
                lq.append(string + restriction.lower())
        for l in list:
            if l != '':
                lq.append(string + l)
    else:
        for l in list:
            lq.append(string + l.title())

    stry_list="".join(lq)
    return(stry_list)

def lookup(query, nextPage):
    try:
        APP_ID = "89232447"
        API_KEY = "ab5a8b2af43c8532c5c061cc41da06dd"
        if nextPage == False:
            response = requests.get(
                f"https://api.edamam.com/api/recipes/v2?type=public&app_id={APP_ID}&app_key={API_KEY}&q={query}")
        else:
            response = requests.get(query)
        response.raise_for_status()

    except requests.RequestException:
        return None

    try:
        result = response.json()
        #Info inside "hits"
        hits_dic = result["hits"]
        recipe_index = []
        next_page_link = result["_links"].get("next", {}).get("href")


        for i in hits_dic:
            link = i["_links"]["self"]["href"]
            label = i["recipe"]["label"]  #name of the recipe
            image = i["recipe"]["image"]
            url = i["recipe"]["url"]      #URL where the recipe is taken from
            calories = round(i["recipe"]["calories"])
            totalTime = i["recipe"]["totalTime"]   #Time range for the total cooking and prep time for a recipe
            ingredientLines = list(i["recipe"]["ingredientLines"])
            #In case there is no type/label, assign []
            cuisineType = list(i["recipe"].get("cuisineType", []))
            mealType = list(i["recipe"].get("mealType", []))
            dishType = list(i["recipe"].get("dishType", []))
            dietLabels = list(i["recipe"].get("dietLabels", []))
            healthLabels = list(i["recipe"].get("healthLabels", []))

            recipe_index.append({
                "link": link,
                "label": label,
                "image": image,
                "url": url,
                "calories": calories,
                "totalTime": totalTime,
                "ingredientLines": ingredientLines,
                "cuisineType": cuisineType,
                "mealType": mealType,
                "dishType": dishType,
                "dietLabels": dietLabels,
                "healthLabels": healthLabels
            })
        return recipe_index, next_page_link
    except (KeyError, TypeError, ValueError):
        return None
