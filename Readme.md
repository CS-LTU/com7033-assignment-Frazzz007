# Stroke Patient Management System

A secure Flask web application for managing stroke patient records using MongoDB and SQLite.

---

## Features

- Doctor login authentication
- Add, edit, delete patient records
- MongoDB for patient data storage
- SQLite for user authentication
- CSRF Protection
- Password hashing
- Pagination and search
- Secure admin account creation via script

---

## System Requirements

- Python 3.9 or higher
- pip
- MongoDB Community Edition
- Git

---

## Installation & Setup (macOS / Linux / Windows)

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd <project-folder>

2. Create and Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows

3. Install Dependencies
pip install flask_sqlalchemy
pip install -r requirements.txt

4. Start MongoDB
macOS (Homebrew)
bash
Copy code
brew services start mongodb-community@7.0
Windows
Start MongoDB from Services or:

mongod
5. Create Admin User (One-Time Only)
bash
Copy code
python scripts/create_admin.py
Default login created by script:

Username: admin
Password: admin

6. Run the Application

bash
Copy code
python app.py
Open in browser:

cpp
Copy code
http://127.0.0.1:5000