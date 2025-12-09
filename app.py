from flask import Flask, render_template, redirect, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from models import db, User
from config import Config
import re

# ---------------- APP CONFIG ----------------

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

with app.app_context():
    db.create_all()

# ---------------- LOGIN MANAGER ----------------

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- INPUT VALIDATION ----------------

def validate_input(text):
    return re.match("^[A-Za-z0-9 .-]+$", text)

# ---------------- AUTH ROUTES ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect("/")

        flash("Invalid credentials", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed = bcrypt.generate_password_hash(
            request.form["password"]
        ).decode("utf-8")

        user = User(
            username=request.form["username"],
            password=hashed
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully")
        return redirect("/")

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect("/")

# ---------------- APP START ----------------

if __name__ == "__main__":
    app.run(debug=True)
