import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, bcrypt, db
from models import User

with app.app_context():

    username = "admin"
    password = "admin"

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        print("User already exists. Choose a different username.")
    else:
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        admin = User(username=username, password=hashed)
        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully")
