from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):  # 👈 Add UserMixin here
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
