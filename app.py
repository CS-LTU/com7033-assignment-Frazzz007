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
            return redirect("/dashboard")

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


# ---------------- PATIENT CRUD ----------------

@app.route("/dashboard")
@login_required
def dashboard():

    patients = mongo.db.patients.find().sort("id", -1)

    return render_template("dashboard.html", patients=patients)



@app.route("/add", methods=["GET", "POST"])
@login_required
def add_patient():

    if request.method == "POST":

        last_patient = mongo.db.patients.find_one(
            sort=[("id", -1)]
        )

        if last_patient:
            new_id = int(last_patient["id"]) + 1
        else:
            new_id = 1

        patient = {
            "id": new_id,
            "gender": request.form["gender"],
            "age": int(request.form["age"]),
            "hypertension": int(request.form["hypertension"]),
            "heart_disease": int(request.form["heart_disease"]),
            "ever_married": request.form["ever_married"],
            "work_type": request.form["work_type"],
            "Residence_type": request.form["Residence_type"],
            "avg_glucose_level": float(request.form["avg_glucose_level"]),
            "bmi": float(request.form["bmi"]),
            "smoking_status": request.form["smoking_status"],
            "stroke": int(request.form["stroke"])
        }

        mongo.db.patients.insert_one(patient)

        flash("Patient added successfully", "success")
        return redirect("/dashboard")

    return render_template("add_patient.html")



@app.route("/delete/<int:id>")
@login_required
def delete_patient(id):

    mongo.db.patients.delete_one({"id": int(id)})

    return redirect("/dashboard")


@app.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_patient(id):

    try:
        patient_id = int(id)
    except:
        flash("Invalid patient ID")
        return redirect("/dashboard")

    patient = mongo.db.patients.find_one({"id": patient_id})

    if not patient:
        flash("Patient not found")
        return redirect("/dashboard")

    if request.method == "POST":
        mongo.db.patients.update_one(
            {"id": patient_id},
            {"$set": dict(request.form)}
        )
        flash("Patient updated successfully")
        return redirect("/dashboard")

    return render_template("edit_patient.html", patient=patient)


@app.route("/patient/<id>")
@login_required
def patient_details(id):
    patient = mongo.db.patients.find_one({"id": id})
    return render_template("patient_details.html", patient=patient)


# ---------------- APP START ----------------

if __name__ == "__main__":
    app.run(debug=True)
