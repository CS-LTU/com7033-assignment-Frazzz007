class Config:    
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    MONGO_URI = "mongodb://admin:admin123@localhost:27017/stroke_db?authSource=admin"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_PERMANENT = False


