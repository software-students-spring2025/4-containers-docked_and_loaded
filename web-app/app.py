"""
flask
"""

import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    UserMixin,
    logout_user,
)

from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
MLC_API_URL = os.getenv("MLC_API_URL", "http://mlc:8000/classify")
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
    return render_template("home.html")


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


@app.route("/logout")
@login_required
def logout():
    """
    logout function
    """
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    """
    profile
    """
    return render_template("profile.html")


@app.route("/game1")
def game1():
    """
    game1
    """
    return render_template("game1.html")


@app.route("/send-to-mlc", methods=["POST"])
@login_required
def send_to_mlc():
    """
    send to mlc
    """
    data = request.get_json()
    image_base64 = data.get("image")

    if not image_base64:
        return jsonify({"error": "No image received"}), 400

    response = requests.post(MLC_API_URL, json={"image": image_base64}, timeout=5)
    response.raise_for_status()
    move = response.json().get("move")

    return jsonify({"move": move})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
