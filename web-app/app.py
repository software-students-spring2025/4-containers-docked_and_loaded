from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"

app.config["MONGO_URI"] = f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/{os.getenv('MONGO_DB')}?authSource=admin"
mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(user_id=str(user["_id"]), username=user["username"])
    return None

@app.route("/")
def home():
    return "Hello! Go to /login or /register"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = mongo.db.users.find_one({"username": username})
        if user and user["password"] == password:
            login_user(User(user_id=str(user["_id"]), username=user["username"]))
            return redirect(url_for("home"))
        return render_template("login.html", message="Invalid username or password.")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user:
            return render_template("register.html", message="Username already exists.")

        user_id = mongo.db.users.insert_one({
            "username": username,
            "password": password
        }).inserted_id

        login_user(User(user_id=str(user_id), username=username))
        return redirect(url_for("dashboard"))

    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
