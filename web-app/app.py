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
    current_user,
)

from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
MLC_API_URL = os.getenv("MLC_API_URL", "http://mlc:8000/classify")
MLC_BOT_URL = os.getenv("MLC_BOT_URL", "http://mlc:8000/bot_play")
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
    ai_response = requests.post(MLC_BOT_URL, json={"_id": current_user.id}, timeout=5)
    ai_response.raise_for_status()
    ai_move = ai_response.json().get("move")

    win_matrix = {1: 3, 2: 1, 3: 2}
    if move == ai_move:
        outcome = "tie"
    elif win_matrix[move] == ai_move:
        outcome = "win"
    else:
        outcome = "loss"

    user_data = mongo.db.users.find_one({"_id": ObjectId(current_user.id)})
    rps_data = user_data.get("rps", {"wins": 0, "losses": 0, "history": []})

    if outcome == "win":
        rps_data["wins"] += 1
    elif outcome == "loss":
        rps_data["losses"] += 1

    rps_data.setdefault("history", []).append(
        {"player_move": move, "ai_move": ai_move, "outcome": outcome}
    )

    mongo.db.users.update_one(
        {"_id": ObjectId(current_user.id)}, {"$set": {"rps": rps_data}}
    )

    return jsonify({"move": move, "ai_move": ai_move, "outcome": outcome})


@app.route("/rps-stats")
@login_required
def rps_stats():
    """
    rpsstats
    """
    user = mongo.db.users.find_one({"_id": ObjectId(current_user.id)})
    stats = user.get("rps", {"wins": 0, "losses": 0})
    return jsonify(stats)


@app.route("/game1h")
@login_required
def game1h():
    """
    game1history"""
    user = mongo.db.users.find_one({"_id": ObjectId(current_user.id)})
    rps_data = user.get("rps", {"history": []})
    return render_template("game1h.html", history=rps_data["history"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
