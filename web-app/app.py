"""
flask
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user,
    UserMixin,
)

from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "your-secret-key"

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    """User class for Flask-Login."""

    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID from the MongoDB"""
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(user_id=str(user["_id"]), username=user["username"])
    return None


@app.route("/")
def root():
    """Redirect to Login"""
    return redirect(url_for("login"))


@app.route("/home")
@login_required
def home():
    """Home"""
    return f"Welcome, {current_user.username}! You are logged in."


@app.route("/login", methods=["GET", "POST"])
def login():
    """login"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = mongo.db.users.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            login_user(User(user_id=str(user["_id"]), username=user["username"]))
            return redirect(url_for("home"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """register"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user:
            flash("Username already exists.", "danger")
            return render_template("register.html")

        user_id = mongo.db.users.insert_one(
            {
                "username": username,
                "password": generate_password_hash(password),
                "history": [],
            }
        ).inserted_id

        login_user(User(user_id=str(user_id), username=username))
        return redirect(url_for("home"))

    return render_template("register.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
