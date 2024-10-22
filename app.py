import os
from flask import Flask, request, render_template, redirect, session, send_from_directory
from flask_session import Session
from cs50 import SQL
from werkzeug.exceptions import NotFound
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_paginate import Pagination, get_page_parameter
from helper import login_required, allowed_file, get_type
import random

app = Flask(__name__)

#configuring cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#configuring database
db = SQL("sqlite:///motive.db")

#configuring uploads of images
UPLOAD_FOLDER = "./static/images"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#list of id's
choice_list = []
data = db.execute("SELECT id FROM quotes")
for _ in data:
    choice_list.append(_["id"])
    
#getting quotes from database
def quote():
    num = random.choice(choice_list)
    data = db.execute("SELECT quote, author FROM quotes WHERE id = ?", num)
    quote = {"quote": data[0]["quote"],
            "author": data[0]["author"]}
    return quote


@app.route("/")
@login_required
def index():
    if request.args.get("search"):
        keyword = f"%{request.args.get('search')}%"
        
        total = db.execute("SELECT COUNT(goal_id) as count FROM attained JOIN goals ON attained.goal_id = goals.id where goal like ? GROUP BY goal_id", keyword)[0]["count"]

        page = request.args.get( get_page_parameter(), type= int, default=1)
        per_page = 15
        offset = (page - 1) * per_page 
        
        goals = db.execute("SELECT goal_id, goal, COUNT(goal_id) as comp, CURRENT_DATE - date_added as posted FROM goals JOIN attained ON goals.id = attained.goal_id WHERE goals.goal like ? GROUP BY goal_id LIMIT ? OFFSET ?",
        keyword, 
        per_page,
        offset)
        
        personal_goals = db.execute("SELECT id FROM goals WHERE user_id = ? AND status ='attained'", session["user_id"])
            
        other_goals = db.execute("SELECT goal_id FROM attained WHERE user_id = ?", session["user_id"])
            
        personal_goals_id_list= [] 
        for i in personal_goals:
            if i:
                    personal_goals_id_list.append(i["id"])
        for j in other_goals:
            if j:
                personal_goals_id_list.append(j["goal_id"])
            
        pagination = Pagination(page = page, per_page = per_page, offset =offset, record_name = 'goals', total = total)
        
    else:
        total = db.execute("SELECT COUNT(goal_id) as count FROM attained GROUP BY goal_id")[0]["count"]

        page = request.args.get( get_page_parameter(), type= int, default=1)
        per_page = 15
        offset = (page - 1) * per_page 
        
        goals = db.execute("SELECT goal_id, goal, COUNT(goal_id) as comp, CURRENT_DATE - date_added as posted FROM goals JOIN attained ON goals.id = attained.goal_id GROUP BY goal_id LIMIT ? OFFSET ?", 
                        per_page,
                        offset)
        
        personal_goals = db.execute("SELECT id FROM goals WHERE user_id = ? AND status ='attained'", session["user_id"])
            
        other_goals = db.execute("SELECT goal_id FROM attained WHERE user_id = ?", session["user_id"])
            
        personal_goals_id_list= [] 
        for i in personal_goals:
            if i:
                    personal_goals_id_list.append(i["id"])
        for j in other_goals:
            if j:
                personal_goals_id_list.append(j["goal_id"])
            
        pagination = Pagination(page = page, per_page = per_page, offset =offset, record_name = 'goals', total = total)
    
    q= quote()
    return render_template("index.html", pagination = pagination, goals = goals, personal_goals_id_list = personal_goals_id_list, quote = q)

@app.route("/login", methods = ["GET","POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template('error.html', issue= 'Absence of Username')

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template('error.html', issue= 'Absence of Password')

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hashed_password"], request.form.get("password")
        ):
            render_template('error.html', issue= 'Logging in')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        q = quote()
        return render_template("login.html", quote = q)
    
@app.route("/logout")
def logout():
        session.clear()
        return redirect("/login")
    
@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        gender = request.form.get("gender")
        password = request.form.get('password')
        pass_confirm = request.form.get("pass_confirm")
        
        if not username:
            return render_template("error.html", issue = "Absence of a username")
        elif not password:
            return render_template("error.html", issue = "Absence of a Password")
        
        if password != pass_confirm:
            return render_template("error.html", issue="password matching")
        elif len(password) < 8:
            return render_template("error.html", issue="password length")
        
        hashed = generate_password_hash(password)
    
        check_for_user = db.execute("SELECT * from users where username = ?", username)
          
        
        if request.files["pfp"]:
            pfp = request.files['pfp']
            if pfp in request.files and '' ==  request.files["pfp"].filename:
                pass
            elif pfp and allowed_file(pfp.filename):
                if len(check_for_user) != 0:
                    return render_template("error.html", issue= "username already existing")
                else:
                    db.execute("INSERT INTO users (username, hashed_password, gender) VALUES (?, ?, ?)", username, hashed, gender)
                    filename = secure_filename(f"{username}_0{session['user_id']}.{get_type(pfp.filename)}")
                    pfp.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    id_query = db.execute("SELECT * FROM users WHERE username = ?", username)
                    session["user_id"] = id_query[0]["id"]
            else:
                return render_template("error.html", issue = "filetype not allowed for profile picture")
        else:
             db.execute("INSERT INTO users (username, hashed_password, gender) VALUES (?, ?, ?)", username, hashed, gender)
             id_query = db.execute("SELECT * FROM users WHERE username = ?", username)
             session["user_id"] = id_query[0]["id"]
        
        return redirect("/")
    
    else:
        q= quote()
        return render_template("register.html", quote = q)
    

@app.route("/profile")
@login_required
def profile():
        info = db.execute("SELECT * FROM users where id = ?", session["user_id"])
        username = info[0]["username"]
        profile_picture = f"{username}_0{info[0]['id']}"
        
        total = db.execute("SELECT COUNT(*) as count FROM goals WHERE user_id = ?", session["user_id"])[0]["count"]
    
        page = request.args.get( get_page_parameter(), type= int, default= 1)
        per_page = 10
        offset = (page-1)*per_page
        
        goals = db.execute("SELECT id, goal, status, CURRENT_DATE - date_added AS posted FROM goals WHERE user_id = ? ORDER BY posted DESC LIMIT ? OFFSET ?", 
            session["user_id"],
            per_page,
            offset)

        personal_goals = db.execute("SELECT id FROM goals WHERE user_id = ? AND status ='attained'", session["user_id"])
            
        other_goals = db.execute("SELECT goal_id FROM attained WHERE user_id = ?", session["user_id"])
            
        personal_goals_id_list= [] 
        for i in personal_goals:
            if i:
                    personal_goals_id_list.append(i["id"])
        for j in other_goals:
            if j:
                personal_goals_id_list.append(j["goal_id"])
        
        goal_count = len(personal_goals_id_list)
        
        pagination = Pagination(page = page, total = total, record_name = "goals", per_page= per_page, offset = offset)
        
        q= quote()
        
        return render_template("profile.html", goals = goals, pagination = pagination, profile_picture = profile_picture, username = username, quote= q, goals_count= goal_count)
        
@app.route("/static/images/<filename>")
@login_required
def send_file(filename):
    try:
        new_filename = f"{filename}.jpg"
        return send_from_directory(app.config["UPLOAD_FOLDER"],new_filename)
    except NotFound:
        try:
            new_filename = f"{filename}.jpeg"
            return send_from_directory(app.config["UPLOAD_FOLDER"],new_filename)
        except NotFound:
            try:
                new_filename = f"{filename}.png"
                return send_from_directory(app.config["UPLOAD_FOLDER"],new_filename)
            except NotFound:
                return send_from_directory(app.config["UPLOAD_FOLDER"],"default_profile.png")
            
@app.route("/attain", methods= ["GET","POST"])
@login_required
def attained():
    if request.form.get("type") == "profile":
        if request.method == "POST":
            id = request.form.get("id")
            try:
                db.execute("INSERT INTO attained (goal_id, user_id) VALUES (?,?)", id, session["user_id"])
                db.execute("UPDATE goals SET status = 'attained' WHERE id = ?", int(id))
                return redirect("/profile")
            except Exception:
                return render_template("error.html", issue= "ADDING YOUR GOAL TO DATABASE")
            
        else: 
            return redirect("/profile")
    
    elif request.form.get("type") == "index":
        if request.method == "POST":
            id = request.form.get("id")
            # try:
            db.execute("INSERT INTO attained (goal_id, user_id) VALUES (?,?)", id, session["user_id"])
            db.execute("UPDATE goals SET status = 'attained' WHERE id = ?", int(id))
            return redirect("/")
            # except Exception:
            #     return render_template("error.html", issue= "ADDING YOUR GOAL TO DATABASE")
        
        else: 
            return redirect("/")
        
    
@app.route("/unattain", methods= ["GET","POST"])
@login_required
def unattained():
    if request.form.get("type") == "profile":
        if request.method == "POST":
            id = request.form.get("id")
            try:
                db.execute("DELETE FROM attained WHERE goal_id = ? and user_id = ?", id, session["user_id"])
                db.execute("UPDATE goals SET status = 'unattained' WHERE id = ?", id)
                return redirect("/profile")
            except Exception:
                return render_template("error.html", issue= "REMOVING YOUR GOAL FROM DATABASE")
            
        else: 
            return redirect("/profile")
            
        
    elif request.form.get("type") == "index":
        if request.method == "POST":
            id = request.form.get("id")
            try:
                db.execute("DELETE FROM attained WHERE goal_id = ? and user_id = ?", id, session["user_id"])
                db.execute("UPDATE goals SET status = 'unattained' WHERE id = ?", id)
                return redirect("/")
            except Exception:
                return render_template("error.html", issue= "REMOVING YOUR GOAL FROM DATABASE")
            
        else: 
            return redirect("/")
        
        
    
    
@app.route("/post", methods= ["GET","POST"])
@login_required
def post():
    if request.method == "POST":
        goal = request.form.get("goal")
        db.execute("INSERT INTO goals (user_id, goal, status) VALUES (?, ?,'unattained')", session["user_id"], goal)
        return redirect("/")
    else: 
        return redirect("/profile")
    
@app.route("/delete", methods= ["GET", "POST"])
@login_required
def remove():
    if request.method == "POST":
        id = request.form.get("id")
        db.execute("DELETE FROM attained WHERE goal_id= ? and user_id = ?; ", id, session["user_id"])
        
        db.execute("DELETE FROM goals WHERE id = ?", id)
        return redirect("/profile")
    else:
        return redirect("/profile")